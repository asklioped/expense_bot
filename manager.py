import time
from db import Database

class ExpenseManager:
    def __init__(self, db_path="expenses.db"):
        self.db = Database(db_path)

    def add_expense(self, user_id: int, amount: float, category: str, note: str=""):
        """Додаємо нову витрату"""
        if amount <= 0:
            raise ValueError("Cума витрат має бути більше нуля")
        timestamp = int(time.time())
        self.db.cursor.execute(
            """
            INSERT INTO expenses (user_id, amount, category, timestamp, note, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, timestamp, note, timestamp)
        )
        self.db.connection.commit()

    def get_total_by_period(self, user_id: int, start_ts: int, end_ts: int=None) -> float:
        "Отримати витрати за період"
        if end_ts == None:
            end_ts = int(time.time())
        self.db.cursor.execute(
            """
            SELECT SUM(amount) FROM expenses WHERE user_id=? AND timestamp BETWEEN ? AND ?
            """,
            (user_id, start_ts, end_ts)
        )
        result = self.db.cursor.fetchone()[0]
        return result or 0.0
    
    def get_today_total(self, user_id: int) -> float:
        """Повертає витрати за сьогодні"""
        now = int(time.time())
        start_of_day = now // 86400 * 86400
        return self.get_total_by_period(user_id, start_of_day)
    
    def get_week_total(self, user_id: int) -> float:
        """Повертає витрати за тиждень"""
        now = int(time.time())
        start_of_week = now - 7 * 86400
        return self.get_total_by_period(user_id, start_of_week, now)

    def get_month_total(self, user_id: int) -> float:
        """Витрати за останній місяць (30 днів)"""
        now = int(time.time())
        start_of_month = now - 30 * 86400
        return self.get_total_by_period(user_id, start_of_month, now)