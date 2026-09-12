import hashlib
import functools

def hash_password(password: str) -> str:
    """Hashes a raw password string using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def require_auth(func):
    """Decorator to protect screens from unauthorized access."""
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.current_user:
            print("[SECURITY WARNING] Unauthorized access attempt blocked.")
            self.current_screen = "login"
            return None
        return func(self, *args, **kwargs)
    return wrapper