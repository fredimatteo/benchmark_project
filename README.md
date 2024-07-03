
# Benchmark Project

Questo progetto confronta le performance di Tortoise ORM e SQLAlchemy in Python per operazioni di base sul database.

## Struttura del Progetto

- `tortoise_benchmark.py`: Script per il benchmark di Tortoise ORM.
- `sqlalchemy_benchmark.py`: Script per il benchmark di SQLAlchemy.
- `requirements.txt`: File delle dipendenze.
- `README.md`: Documentazione del progetto.

## Istruzioni per l'Utilizzo

1. Crea un ambiente virtuale:
    ```bash
    python -m venv venv
    ```

2. Attiva l'ambiente virtuale:
    - Su macOS/Linux:
        ```bash
        source venv/bin/activate
        ```
    - Su Windows:
        ```bash
        .\venv\Scripts\activate
        ```

3. Installa le dipendenze:
    ```bash
    pip install -r requirements.txt
    ```

4. Esegui i benchmark:
    - Per Tortoise ORM:
        ```bash
        python tortoise_benchmark.py
        ```
    - Per SQLAlchemy:
        ```bash
        python sqlalchemy_benchmark.py
        ```
