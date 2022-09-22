from blacksheep.server.controllers import APIController, get, post
from dataclasses import dataclass
from blacksheep.server.authorization import auth
from blacksheep import text, json
from auth.data import Authenticated, JWTPayload, Roles
from piccolo.apps.user.tables import BaseUser
from auth.jwt import JsonWebToken


@dataclass
class LoginInput:
    username: str
    password: str


class User(APIController):
    @classmethod
    def version(cls):
        return "v1"

    # @auth(Roles.ADMIN)
    # @auth(Authenticated)
    @post("/login")
    async def login(self, login: LoginInput, jwt: JsonWebToken):
        if not (id := await BaseUser.login(username=login.username, password=login.password)):
            return json({"status": False, "message": "Invalid username or password"})
        user: BaseUser = await BaseUser.objects().get(BaseUser.id == id)
        return json({"status": True,
                     "token": jwt.creact_jwt_token(JWTPayload(id=id,
                                                              name=user.username,
                                                              email=user.email,
                                                              role=Roles.ADMIN if user.superuser or user.admin else Roles.USER
                                                              ))})

    # @auth(Authenticated)
    # @post("/foo")
    # async def create_foo(self, foo: CreateFooInput):
    #     return json({"status": True})
