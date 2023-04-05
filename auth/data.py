from dataclasses import dataclass, field
import time


class Roles:
    ADMIN = "ADMIN"
    SUPERADMIN = "SUPERADMIN"
    USER = "USER"
    BANNED = "BANNED"


Authenticated = "authenticated"


@dataclass
class JWTPayload:
    id: int
    name: str
    email: str = field(default=None)
    is_superuser: bool = field(default=False)
    is_admin: bool = field(default=False)
    iat: int = field(default_factory=lambda: int(time.time()))
    exp: int = field(default_factory=lambda: int(time.time()) + 604800)

    def get(self, key):
        return getattr(self, key)
