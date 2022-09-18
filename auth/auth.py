from typing import Optional

from blacksheep.messages import Request
from blacksheep.server import Application
from blacksheep.server.authorization import Policy
from guardpost.asynchronous.authentication import AuthenticationHandler, Identity
from guardpost.authorization import AuthorizationContext
from guardpost.common import AuthenticatedRequirement
from guardpost.synchronous.authorization import Requirement
from .jwt import Encryptor

class AuthHandler(AuthenticationHandler):
    def __init__(self,encryptor:Encryptor):
        self.encryptor = encryptor
    
    async def authenticate(self, context: Request) -> Optional[Identity]:
        header_value = context.get_first_header(b'Authorization')
        if header_value:
            try:
                header_value = header_value.decode().replace('Bearer ', '')
                info = self.encryptor.validate_jwt_token(header_value)
                assert isinstance(info,dict)
                assert 'ID' in info
                if info['state'] != 0:
                    raise Exception('Invalid state')
                if info['role'] == 1:
                    raise Exception('You are not admin')
                if info['role'] == 2:
                    raise Exception('You are not superadmin')
                context.identity = Identity(info,"scheme")
            except:
                context.identity = None
        return context.identity

class AdminRequirement(Requirement):
    def handle(self, context: AuthorizationContext):
        identity = context.identity

        if identity is not None and identity.claims.get("role") == 1:
            context.succeed(self)

class AdminPolicy(Policy):
    def __init__(self):
        super().__init__("admin", AdminRequirement())

class Init:
    def __init__(self, app: Application) -> None:
        Authenticated = "authenticated"
        provider =  app.services.build_provider()
        app.use_authentication().add(AuthHandler(encryptor = provider.get(Encryptor)))
        app.use_authorization().add(Policy(Authenticated, AuthenticatedRequirement())).add(AdminPolicy())