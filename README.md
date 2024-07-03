# Benchmark Project: Tortoise ORM vs SQLAlchemy

This project compares the performance of Tortoise ORM and SQLAlchemy in Python for basic database operations, including inserts, reads, updates, and deletes. The results are compared to determine the best ORM for each operation.

## Project Structure

- `main.py`: Main script to run the benchmarks and compare the results.
- `requirements.txt`: Dependencies file.
- `README.md`: Project documentation.

## Dependencies

To install the required dependencies, use:

```bash
pip install -r requirements.txt
```

# Detailed Analysis

### Single Insert

- **SQLAlchemy:** 0.239925 seconds
- **Tortoise:** 0.393344 seconds
- **Winner:** SQLAlchemy

### Bulk Insert

- **SQLAlchemy:** 0.067857 seconds
- **Tortoise:** 0.021961 seconds
- **Winner:** Tortoise

### Read

- **SQLAlchemy:** 0.026788 seconds
- **Tortoise:** 0.017947 seconds
- **Winner:** Tortoise

### Read with Join

- **SQLAlchemy:** 0.026055 seconds
- **Tortoise:** 0.080005 seconds
- **Winner:** SQLAlchemy

### Update

- **SQLAlchemy:** 0.205512 seconds
- **Tortoise:** 0.372545 seconds
- **Winner:** SQLAlchemy

### Delete

- **SQLAlchemy:** 0.026199 seconds
- **Tortoise:** 0.004393 seconds
- **Winner:** Tortoise

## Pros and Cons

### Tortoise ORM

**Pros:**

- **Bulk Insert:** Significantly faster for bulk insert operations.
- **Read Users:** Faster for simple read operations.
- **Delete Query:** Exceptionally fast for delete operations.

**Cons:**

- **Single Insert:** Slower for single insert operations.
- **Read with Join:** Slower for read operations with joins.
- **Update Query:** Slower for update operations.

### SQLAlchemy

**Pros:**

- **Single Insert:** Faster for single insert operations.
- **Read with Join:** Faster for read operations with joins.
- **Update Query:** Faster for update operations.

**Cons:**

- **Bulk Insert:** Slower for bulk insert operations.
- **Read Users:** Slightly slower for simple read operations.
- **Delete Query:** Slower for delete operations.

# Conclusion

This project helps in understanding the performance differences between Tortoise ORM and SQLAlchemy for various database operations. The benchmark results provide insights into which ORM might be better suited for different types of operations.

For projects that require fast bulk inserts and simple reads or deletes, Tortoise ORM may be a better choice. On the other hand, SQLAlchemy shows better performance for single inserts, complex reads with joins, and updates. The choice of ORM should be guided by the specific requirements and performance characteristics of your application.
