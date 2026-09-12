import time
from utils.auth import hash_password

class User:
    def __init__(self, username: str, password_hash: str, streak: int = 1, last_login_day: int = 0, total_points: int = 0, last_daily: float = 0.0, status: str = "offline"):
        self.username = username
        self._password_hash = password_hash
        self.streak = streak
        self.last_login_day = last_login_day  # Stores epoch day index
        self.total_points = total_points
        self.last_daily = last_daily
        self.status = status  # "online", "offline", "engaged - playing another game"

    def verify_password(self, password: str) -> bool:
        return self._password_hash == hash_password(password)

    def update_streak(self) -> bool:
        """Updates weekly login streak. Resets if a day was skipped."""
        current_day = int(time.time() // 86400)
        
        if self.last_login_day == 0:
            self.streak = 1
        elif current_day - self.last_login_day == 1:
            self.streak = (self.streak % 7) + 1  # Cap/reset weekly at 7
        elif current_day - self.last_login_day > 1:
            self.streak = 1  # Skipped a day -> reset

        self.last_login_day = current_day
        return True

    def add_points(self, points: int):
        self.total_points += points

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password_hash": self._password_hash,
            "streak": self.streak,
            "last_login_day": self.last_login_day,
            "total_points": self.total_points,
            "last_daily": self.last_daily,
            "status": self.status
        }

    @classmethod
    def create_new(cls, username: str, raw_password: str):
        u = cls(username, hash_password(raw_password), streak=1, last_login_day=int(time.time() // 86400), total_points=0, last_daily=0.0, status="online")
        return u