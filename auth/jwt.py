from dataclasses import asdict
import jwt
import os
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization
from blake3 import blake3
from auth.data import JWTPayload


class JsonWebToken:
    def __init__(self) -> None:
        self.init()

    def init(self) -> None:
        if os.path.exists("key"):
            with open("key", "rb") as f:
                self.key = f.read()
                self.private_key = ed25519.Ed25519PrivateKey.from_private_bytes(
                    self.key
                )
                self.public_key = self.private_key.public_key()
        else:
            self.private_key = ed25519.Ed25519PrivateKey.generate()
            self.public_key = self.private_key.public_key()
            self.key = self.private_key.private_bytes(
                encoding=serialization.Encoding.Raw,
                format=serialization.PrivateFormat.Raw,
                encryption_algorithm=serialization.NoEncryption(),
            )
            with open("key", "wb") as f:
                f.write(self.key)

    def hash_password(self, password: str) -> str:
        return blake3(password.encode(), key=self.key).hexdigest(length=128)

    def creact_jwt_token(self, payload: JWTPayload) -> str:
        return jwt.encode(asdict(payload), self.private_key, algorithm="EdDSA")

    def validate_jwt_token(self, token: str) -> dict:
        return jwt.decode(token, self.public_key, algorithms=["EdDSA"])
