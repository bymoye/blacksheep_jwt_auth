from typing import Optional

from blacksheep.messages import Request
from blacksheep.server.authorization import Policy
from guardpost.asynchronous.authentication import AuthenticationHandler, Identity
from guardpost.authorization import AuthorizationContext
from guardpost.synchronous.authorization import Requirement
from .jwt import JsonWebToken
from .data import Roles


class AuthHandler(AuthenticationHandler):

    def __init__(self, jwt: JsonWebToken):
        self.jwt = jwt

    async def authenticate(self, context: Request) -> Optional[Identity]:
        if header_value := context.get_first_header(b'Authorization'):
            try:
                assert header_value.startswith(b'Bearer ')
                token = header_value[7:].decode()
                info = self.jwt.validate_jwt_token(token)
                context.identity = Identity(info, "scheme")
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


class SuperAdminRequirement(Requirement):

    def handle(self, context: AuthorizationContext):
        identity = context.identity
        if identity and identity.has_claim_value('role', Roles.SUPERADMIN):
            context.succeed(self)


class SuperAdminPolicy(Policy):

    def __init__(self):
        super().__init__(Roles.SUPERADMIN, SuperAdminRequirement())