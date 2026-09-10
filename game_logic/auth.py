class AccountManager:
    def __init__(self):
        self.users = {}

    def register_user(self, username: str, age: int) -> bool:
        if not username or not isinstance(username, str):
            raise ValueError("Invalid username")
        if age < 14:
            raise ValueError("User must be at least 14 years old")
        if username in self.users:
            return False
            
        self.users[username] = {"age": age, "active": True}
        return True

    def is_active(self, username: str) -> bool:
        user = self.users.get(username)
        if not user:
            return False
        return user["active"]