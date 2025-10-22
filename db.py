import sqlite3
import logging
from pathlib import Path

class Database:
    def __init__(self, db_path="expenses.db"):
        self.db_path = Path(db_path)
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        logging.info(f"Підключення до бази даних {self.db_path}")
        self._create_table()


    def _create_table(self):
        """Створюємо таблицю expenses, якщо її нема """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                timestamp INTEGER NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.connection.commit()
        logging.info("Перевірено наявність таблиці 'expenses'")
