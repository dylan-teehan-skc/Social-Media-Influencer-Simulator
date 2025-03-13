from src.patterns.interfaces.user_decorator import UserDecorator
from functools import wraps


class VerifiedUser(UserDecorator):
    def get_handle(self) -> str:
        """Add verification checkmark to handle."""
        return f"{self._user.handle} ✔️"

    def get_bio(self) -> str:
        """Add verification tag to bio."""
        return f"{self._user.bio} (Verified)"
        
    def __getattr__(self, name):
        """Forward all other attributes and methods to the wrapped user."""
        attr = getattr(self._user, name)
        
        # If it's a signal, return it directly
        if hasattr(attr, 'emit'):
            return attr
            
        # If it's a method, wrap it to preserve the original signature
        if callable(attr):
            @wraps(attr)
            def wrapper(*args, **kwargs):
                # If no post argument is provided for attach/notify, add None
                if name in ['attach', 'notify'] and len(args) == 1:
                    return attr(args[0], None)
                return attr(*args, **kwargs)
            return wrapper
            
        return attr
