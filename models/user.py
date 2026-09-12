import time
from utils.auth import hash_password

class User:
    """Represents a user in the 101 Game ecosystem."""
    def __init__(self, username: str, password_hash: str, streak: int = 1, last_login_day: int = 0, total_points: int = 0, last_daily: float = 0.0, status: str = "offline"):
        self.username = username
        self._password_hash = password_hash  # Encapsulated property
        self.streak = streak
        self.last_login_day = last_login_day  # Epoch day index (time.time() // 86400)
        self.total_points = total_points
        self.last_daily = last_daily
        self.status = status  # States: "online", "offline", "engaged - playing another game"

    def verify_password(self, password: str) -> bool:
        """Verifies given raw password against stored hash."""
        return self._password_hash == hash_password(password)

    def update_streak(self) -> bool:
        """Calculates weekly streak logic on login.
        
        Increments streak if logged in on consecutive days.
        Resets streak to 1 if a day was skipped.
        """
        current_day = int(time.time() // 86400)
        
        if self.last_login_day == 0:
            self.streak = 1
        elif current_day - self.last_login_day == 1:
            # Consecutive day: increment streak up to 7
            self.streak = (self.streak % 7) + 1
        elif current_day - self.last_login_day > 1:
            # Skipped a day or more: reset streak
            self.streak = 1

        self.last_login_day = current_day
        return True

    def set_status(self, new_status: str):
        """Updates real-time activity status."""
        valid_statuses = ["online", "offline", "engaged - playing another game"]
        if new_status in valid_statuses:
            self.status = new_status

    def to_dict(self) -> dict:
        """Serializes user instance to JSON dictionary."""
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
        """Factory method for initial user registration."""
        current_day = int(time.time() // 86400)
        return cls(
            username=username,
            password_hash=hash_password(raw_password),
            streak=1,
            last_login_day=current_day,
            total_points=0,
            last_daily=0.0,
            status="online"
        )