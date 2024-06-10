import sqlite3
import os
import random
from app.utils.logger import logger

class DatabaseService:
    def __init__(self):
        data_directory = os.path.join(os.path.dirname(__file__), "data")

        if not os.path.exists(data_directory):
            os.makedirs(data_directory)

        self.path = os.path.join(data_directory, "database.db")
        self._initialize_database()

    def _initialize_database(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                nicknames TEXT,
                points INTEGER DEFAULT 0,
                exp INTEGER DEFAULT 0,
                total_exp INTEGER DEFAULT 0,
                level INTEGER DEFAULT 1
            )""")
            # Check if 'total_exp' column exists
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'total_exp' not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN total_exp INTEGER DEFAULT 0")
                cursor.execute("UPDATE users SET total_exp = exp + ((level - 1) * 100)")
            conn.commit()

    def add_user(self, user):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT 1 FROM users WHERE id = ?", (user.id,))
            user_exists = cursor.fetchone()
            
            if not user_exists:
                # User does not exist, insert them
                cursor.execute("""
                INSERT OR IGNORE INTO users (id, name, nicknames, points, exp, total_exp, level)
                VALUES (?, ?, ?, 0, 0, 0, 1)""", (user.id, user.name, user.name))
                conn.commit()
                logger.info(f"User added: {user.name} (ID: {user.id})")

    def add_point(self, user_id: int):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET points = points + 1 WHERE id = ?", (user_id,))
            conn.commit()

    def subtract_point(self, user_id: int):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET points = points - 1 WHERE id = ?", (user_id,))
            conn.commit()

    def get_points(self, user_id: int) -> int:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT points FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0

    def add_nickname(self, user_id: int, nickname: str):
        if not nickname:
            return

        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nicknames FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                nicknames = result[0].split(',')
                if nickname not in nicknames:
                    nicknames.append(nickname)
                    cursor.execute("UPDATE users SET nicknames = ? WHERE id = ?", (",".join(nicknames), user_id))
                    conn.commit()

    def get_nicknames(self, user_id: int) -> list:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nicknames FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            return result[0].split(',') if result else []

    def get_exp(self, user_id: int) -> int:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT exp FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_total_exp(self, user_id: int) -> int:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT total_exp FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            return result[0] if result else 0

    def add_exp(self, user_id: int, amount: int) -> tuple:
        level_up = False
        level_down = False
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT exp, level, total_exp FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                exp, level, total_exp = result
                print(f"Initial values - exp: {exp}, level: {level}, total_exp: {total_exp}")

                total_exp += amount
                if total_exp < 0:
                    total_exp = 0
                
                # Calculate new level based on total experience
                new_level = self.calculate_level(total_exp)
                exp_in_level = total_exp - self.experience_to_reach_level(new_level)
                
                if new_level > level:
                    level_up = True
                elif new_level < level:
                    level_down = True
                
                cursor.execute("UPDATE users SET exp = ?, total_exp = ?, level = ? WHERE id = ?", (exp_in_level, total_exp, new_level, user_id))
                conn.commit()
                print(f"Updated values - exp_in_level: {exp_in_level}, total_exp: {total_exp}, new_level: {new_level}, level_up: {level_up}, level_down: {level_down}")
            else:
                print(f"User {user_id} not found.")
        return level_up, level_down

    def experience_to_reach_level(self, level: int) -> int:
        """Calculates the total experience required to reach the given level."""
        return sum((i * 100) for i in range(1, level))

    def calculate_level(self, total_exp: int) -> int:
        """Calculates the level based on total experience."""
        level = 1
        while total_exp >= self.experience_to_reach_level(level + 1):
            level += 1
        return level



    def get_level_info(self, user_id: int) -> tuple:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT level, total_exp FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if result:
                level, total_exp = result
                exp_in_level = total_exp - self.experience_to_reach_level(level)
                return level, f"{exp_in_level}/{level * 100}", total_exp
            return 0, "0/0", 0



    def get_leaderboard(self) -> str:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name, level, exp FROM users ORDER BY level DESC, exp DESC LIMIT 10")
            results = cursor.fetchall()
            leaderboard = "\n".join([f"{i + 1}. {name} | Lv. {level} | Exp. {exp}" for i, (name, level, exp) in enumerate(results)])
            return leaderboard

    def add_picture(self, type: str, link: str):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pictures (type, link) VALUES (?, ?)", (type, link))
            conn.commit()

    def get_random_picture(self, type: str) -> str:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT link FROM pictures WHERE type = ?", (type,))
            results = cursor.fetchall()
            if results:
                return random.choice(results)[0]
            return None

    def get_pictures(self, type: str) -> list:
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT link FROM pictures WHERE type = ?", (type,))
            results = cursor.fetchall()
            return [result[0] for result in results]

    def list_users(self):
        with sqlite3.connect(self.path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, level, exp, total_exp FROM users")
            results = cursor.fetchall()
            for user in results:
                logger.debug(user)
