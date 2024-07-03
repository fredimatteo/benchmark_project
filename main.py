import time
import asyncio
from tortoise import Tortoise, fields
from tortoise.models import Model
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker


class UserTortoise(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)

class AddressTortoise(Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.UserTortoise', related_name='addresses')
    address = fields.CharField(max_length=255)

async def init_tortoise():
    await Tortoise.init(db_url='sqlite://:memory:', modules={'models': ['__main__']})
    await Tortoise.generate_schemas()
    
async def close_tortoise():
    await Tortoise.close_connections()

async def benchmark_tortoise() -> dict:
    result = {}
    await init_tortoise()
    
    # Single Insert Users
    start_time = time.time()
    for i in range(10000):
        user = UserTortoise(name=f'User {i}')
        await user.save()
    result['single_insert'] = time.time() - start_time
    
    # Bulk Insert Users
    await UserTortoise.all().delete()  # Pulisce il database per evitare conflitti
    start_time = time.time()
    users = [UserTortoise(name=f'User {i}') for i in range(10000)]
    await UserTortoise.bulk_create(users)
    result['bulk_insert'] = time.time() - start_time

    # Insert Addresses
    start_time = time.time()
    users = await UserTortoise.all()
    for i, user in enumerate(users):
        address = AddressTortoise(user=user, address=f'Address {i}')
        await address.save()
    
    # Read Users
    start_time = time.time()
    users = await UserTortoise.all()
    result['read_users'] = time.time() - start_time
    
    # Read with Join
    start_time = time.time()
    users_with_addresses = await UserTortoise.all().prefetch_related('addresses')
    result['read_with_join'] = time.time() - start_time
    
    # Update Addresses
    start_time = time.time()
    for user in users_with_addresses:
        for address in user.addresses:
            address.address = 'Updated Address'
            await address.save()
    result['update_query'] = time.time() - start_time
    
    # Delete
    start_time = time.time()
    await AddressTortoise.all().delete()
    await UserTortoise.all().delete()
    result['delete_query'] = time.time() - start_time
    
    await close_tortoise()
    return result 


Base = declarative_base()

class UserSQLAlchemy(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class AddressSQLAlchemy(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    address = Column(String)
    user = relationship('UserSQLAlchemy', back_populates='addresses')

UserSQLAlchemy.addresses = relationship('AddressSQLAlchemy', order_by=AddressSQLAlchemy.id, back_populates='user')

engine = create_engine('sqlite:///:memory:')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

def benchmark_sqlalchemy() -> dict:
    result = {}
    session = Session()

    # Single Insert Users
    start_time = time.time()
    for i in range(10000):
        user = UserSQLAlchemy(name=f'User {i}')
        session.add(user)
    session.commit()
    result['single_insert'] = time.time() - start_time
    
    # Bulk Insert Users
    session.query(UserSQLAlchemy).delete()  # Pulisce il database per evitare conflitti
    session.commit()
    start_time = time.time()
    users = [UserSQLAlchemy(name=f'User {i}') for i in range(10000)]
    session.bulk_save_objects(users)
    session.commit()
    result['bulk_insert'] = time.time() - start_time

    # Insert Addresses
    start_time = time.time()
    users = session.query(UserSQLAlchemy).all()
    for i, user in enumerate(users):
        address = AddressSQLAlchemy(user=user, address=f'Address {i}')
        session.add(address)
    session.commit()
    
    # Read Users
    start_time = time.time()
    users = session.query(UserSQLAlchemy).all()
    result['read_users'] = time.time() - start_time
    
    # Read with Join
    start_time = time.time()
    users_with_addresses = session.query(UserSQLAlchemy).join(AddressSQLAlchemy).all()
    result['read_with_join'] = time.time() - start_time
    
    # Update Addresses
    start_time = time.time()
    addresses = session.query(AddressSQLAlchemy).all()
    for address in addresses:
        address.address = 'Updated Address'
    session.commit()
    result['update_query'] = time.time() - start_time
    
    # Delete
    start_time = time.time()
    session.query(AddressSQLAlchemy).delete()
    session.query(UserSQLAlchemy).delete()
    session.commit()
    result['delete_query'] = time.time() - start_time
    
    return result

alchemy_result = benchmark_sqlalchemy()
tortoise_result = asyncio.run(benchmark_tortoise())

def compare_results(tortoise_results, sqlalchemy_results):
    comparison = {}
    for key in tortoise_results:
        if tortoise_results[key] < sqlalchemy_results[key]:
            comparison[key] = f"Tortoise è migliore ({tortoise_results[key]:.6f} s vs {sqlalchemy_results[key]:.6f} s)"
        else:
            comparison[key] = f"SQLAlchemy è migliore ({sqlalchemy_results[key]:.6f} s vs {tortoise_results[key]:.6f} s)"
    return comparison


comparison = compare_results(tortoise_result, alchemy_result)

for k, v in comparison.items():
    print(f'{k}:\n{v}')
    print('')
