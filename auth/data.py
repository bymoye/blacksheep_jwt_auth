from dataclasses import dataclass, field
import enum
import time

class Roles:
    ADMIN = "ADMIN"
    USER = "USER"
    BANNED = "BANNED"


Authenticated = "authenticated"

@dataclass
class JWTPayload:
    id: int
    name: str
    email: str = field(default=None)
    role: Roles = field(default=Roles.USER)
    iat: int = field(default_factory=lambda: int(time.time()))
    exp: int = field(default_factory=lambda: int(time.time()) + 604800)
    
    def get(self, key):
        return self.__dict__.get(key)