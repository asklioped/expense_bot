import sqlite3
import logging
from pathlib import Path

class Database:
    def __init__(self, db_path="expensive.db"):
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
                note TEXT,
                created_at INTEGER NOT NULL
            )
            """
        )
        self.connection.commit()
        logging.info("Перевірено наявність таблиці 'expenses'")


    def add_expense(self, user_id: int, amount: float, category: str, note: str = ""):
        """Додавання витрати до таблиці"""
        timestamp = int(sqlite3.time.time())
        self.cursor.execute(
            """
            INSERT INTO expenses (user_id, amount, category, timestamp, note, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, timestamp, note, timestamp)
        )
        self.connection.commit()


    def get_expenses(self, user_id: int, start_ts: int = 0, end_ts: int = None):
        """Отримати витрати користувача за певний період"""
        if end_ts is None:
            end_ts = int(sqlite3.time.time())
        self.cursor.execute(
            "SELECT * FROM expenses WHERE user_id=? AND timestamp BETWEEN ? AND ?",
            (user_id, start_ts, end_ts)
        )
        return self.cursor.fetchall()