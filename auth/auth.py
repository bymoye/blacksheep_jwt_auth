from typing import Optional

from blacksheep.messages import Request
from blacksheep.server import Application
from blacksheep.server.authorization import Policy
from guardpost.asynchronous.authentication import AuthenticationHandler, Identity
from guardpost.authorization import AuthorizationContext
from guardpost.common import AuthenticatedRequirement
from guardpost.synchronous.authorization import Requirement
from .jwt import JsonWebToken
from .data import JWTPayload, Roles, Authenticated


class AuthHandler(AuthenticationHandler):
    def __init__(self, jwt: JsonWebToken):
        self.jwt = jwt

    async def authenticate(self, context: Request) -> Optional[Identity]:
        if header_value := context.get_first_header(b'Authorization'):
            try:
                header_value = header_value.decode().replace('Bearer ', '')
                info = self.jwt.validate_jwt_token(header_value)
                context.identity = Identity(info, "scheme")
                # context.identity = info
            except:
                context.identity = Identity(None)
        return context.identity


class AdminRequirement(Requirement):
    def handle(self, context: AuthorizationContext):
        identity = context.identity

        if identity and identity.has_claim_value('role', Roles.ADMIN):
            context.succeed(self)


class AdminPolicy(Policy):
    def __init__(self):
        super().__init__(Roles.ADMIN, AdminRequirement())


class Init:
    def __init__(self, app: Application) -> None:
        provider = app.services.build_provider()
        app.use_authentication().add(AuthHandler(encryptor=provider.get(JsonWebToken)))
        app.use_authorization().add(
            Policy(Authenticated, AuthenticatedRequirement())).add(AdminPolicy())
