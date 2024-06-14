import sqlite3
import os
from app.services.database_service import DatabaseService
from app.utils.logger import logger
class CasinoJar:
    def __init__(self):
        self.database_service = DatabaseService()
        self._initialize_jar_table()

    def _initialize_jar_table(self):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS casino_jar (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                points INTEGER DEFAULT 0,
                user_id INTEGER NOT NULL
            )""")
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS jar_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                points INTEGER,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )""")
            # Check if columns full_wins and partial_wins exist, if not add them
            cursor.execute("PRAGMA table_info(jar_history)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'full_wins' not in columns:
                cursor.execute("ALTER TABLE jar_history ADD COLUMN full_wins INTEGER DEFAULT 0")
            if 'partial_wins' not in columns:
                cursor.execute("ALTER TABLE jar_history ADD COLUMN partial_wins INTEGER DEFAULT 0")
            conn.commit()

    def add_to_jar(self, user_id, points):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO casino_jar (user_id, points) VALUES (?, ?)", (user_id, points))
            cursor.execute("INSERT INTO jar_history (user_id, points, action) VALUES (?, ?, 'lose')", (user_id, points))
            conn.commit()
    
    def add_winning_combination(self, user_id, full_wins=0, partial_wins=0):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO jar_history (user_id, full_wins, partial_wins, action) VALUES (?, ?, ?, 'nothing')", (user_id, full_wins, partial_wins))
            conn.commit()

    def get_from_jar(self, user_id):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(points) FROM casino_jar")
            total_points = cursor.fetchone()[0] or 0
            if total_points > 0:
                cursor.execute("INSERT INTO casino_jar (user_id, points) VALUES (?, ?)", (user_id, -total_points))
                cursor.execute("INSERT INTO jar_history (user_id, points, action) VALUES (?, ?, 'win')", (user_id, total_points))
                conn.commit()
                return total_points
            return 0  # No points in the jar

    def get_jar_total(self):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(points) FROM casino_jar")
            return cursor.fetchone()[0] or 0

    def get_last_winner(self):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT user_id, points, timestamp FROM jar_history WHERE action='win' ORDER BY timestamp DESC LIMIT 1")
            return cursor.fetchone()

    def get_top_losers(self, limit=5):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT user_id, SUM(points) as total_lost, COUNT(*) as lose_count 
            FROM jar_history 
            WHERE action='lose' 
            GROUP BY user_id 
            ORDER BY total_lost DESC 
            LIMIT ?""", (limit,))
            return cursor.fetchall()

    def get_top_winners_with_counts(self, limit=5):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT user_id, SUM(points) as total_won, COUNT(*) as win_count 
            FROM jar_history 
            WHERE action='win' 
            GROUP BY user_id 
            ORDER BY total_won DESC 
            LIMIT ?""", (limit,))
            return cursor.fetchall()
        
    def get_winning_combination_counts(self):
        with sqlite3.connect(self.database_service.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT user_id, SUM(full_wins) as total_full_wins, SUM(partial_wins) as total_partial_wins 
            FROM jar_history 
            GROUP BY user_id 
            ORDER BY total_full_wins DESC, total_partial_wins DESC""")
            return cursor.fetchall()
