import time

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from db import Database
from config import tz_name


class ExpenseManager:
    def __init__(self, db_path="expenses.db"):
        self.db = Database(db_path)


    def add_expense(self, user_id: int, amount: float, category: str, tz_name: str = "Europe/Kyiv"):
        """Додаємо нову витрату"""
        timestamp = int(time.time())
        date_str = self.local_timestamp_txt(self.local_timestamp(tz_name))#datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y %H:%M:%S")
        self.db.cursor.execute(
            """
            INSERT INTO expenses (user_id, amount, category, timestamp, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, amount, category, timestamp, date_str)
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
    

    def local_timestamp(self, tz_name: str = "Europe/Kyiv") -> int: 
        "Вираховує timestamp в UTC, а повертає його з врахуванням місцевого часу"
        local_time = datetime.now(ZoneInfo(tz_name))
        return int(local_time.timestamp())
    

    def local_timestamp_txt(self, local_timestamp: int, tz_name: str = "Europe/Kyiv") -> str:
        "Бере лолкальний timestamp, а повертає його текстове представлення"
        dt = datetime.fromtimestamp(local_timestamp, ZoneInfo(tz_name))
        return dt.strftime("%d-%m-%Y %H:%M:%S")
    

    def get_today_total(self, user_id: int) -> float:
        """Повертає витрати за сьогодні"""
        now = self.local_timestamp(tz_name)
        start_of_day = now // 86400 * 86400
        return self.get_total_by_period(user_id, start_of_day)

    
    def get_week_delta(self, user_id: int, tz_name: str = "Europe/Kyiv") -> float:
        """Повертає витрати з початку поточного тижня (понеділок 00:00)"""
        
        # поточний локальний datetime
        now_dt = datetime.now(ZoneInfo(tz_name))
        
        # який сьогодні день тижня (понеділок=0)
        start_of_week_dt = now_dt - timedelta(days=now_dt.weekday())
        
        # робимо час 00:00:00
        start_of_week_dt = datetime(start_of_week_dt.year,
                                    start_of_week_dt.month,
                                    start_of_week_dt.day,
                                    tzinfo=ZoneInfo(tz_name))
        
        # перетворюємо datetime у int timestamp
        start_of_week_ts = int(start_of_week_dt.timestamp())
        now_ts = int(now_dt.timestamp())
        
        # передаємо в функцію підрахунку
        return self.get_total_by_period(user_id, start_of_week_ts, now_ts)


# Треба переробити
    # def get_month_total(self, user_id: int) -> float:
    #     """Витрати за останній місяць (30 днів)"""
    #     now = int(time.time())
    #     start_of_month = now - 30 * 86400
    #     return self.get_total_by_period(user_id, start_of_month, now)

    def get_month_total(self, user_id: int) -> float:
        """Витрати з початку поточного місяця"""
        now = datetime.now()

        # Початок поточного місяця (1 число о 00:00)
        start_of_month = datetime(year=now.year, month=now.month, day=1)

        # Перетворюємо у timestamp (секунди з 1970 року)
        start_of_month_ts = int(start_of_month.timestamp())
        now_ts = int(time.time())

        return self.get_total_by_period(user_id, start_of_month_ts, now_ts)