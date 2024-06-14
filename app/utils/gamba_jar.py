import sqlite3
import os

class CasinoJar:
    def __init__(self, database_service):
        self.database_service = database_service
        self._initialize_jar_table()

    def _initialize_jar_table(self):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS casino_jar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                points INTEGER DEFAULT 0
            )""")
            conn.commit()

    def add_to_jar(self, points):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO casino_jar (points) VALUES (?)", (points,))
            conn.commit()

    def get_from_jar(self, points):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(points) FROM casino_jar")
            total_points = cursor.fetchone()[0] or 0
            if total_points >= points:
                cursor.execute("INSERT INTO casino_jar (points) VALUES (?)", (-points,))
                conn.commit()
                return points
            return 0  # Not enough points in the jar

    def get_jar_total(self):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(points) FROM casino_jar")
            return cursor.fetchone()[0] or 0
