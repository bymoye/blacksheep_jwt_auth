from typing import Optional
from blacksheep.server.controllers import APIController, get, post
from dataclasses import dataclass
from blacksheep.server.authorization import auth
from blacksheep import text, json
from auth.data import Authenticated, JWTPayload, Roles
from piccolo.apps.user.tables import BaseUser
from auth.jwt import JsonWebToken
from guardpost.authentication import Identity


@dataclass
class UserInput:
    username: str
    password: str


@dataclass
class CreateUserInput(UserInput):
    email: str


class User(APIController):

    @classmethod
    def version(cls):
        return "v1"

    # @auth(Roles.ADMIN)
    # @auth(Authenticated)
    @post("/login")
    async def login(self, login: UserInput, jwt: JsonWebToken):
        if not (id := await BaseUser.login(username=login.username,
                                           password=login.password)):
            return json({
                "status": False,
                "message": "Invalid username or password"
            })
        user: BaseUser = await BaseUser.objects().get(BaseUser.id == id)
        return json({
            "status":
            True,
            "token":
            jwt.creact_jwt_token(
                JWTPayload(id=id,
                           name=user.username,
                           email=user.email,
                           role=Roles.ADMIN
                           if user.superuser or user.admin else Roles.USER))
        })

    @post("/create")
    async def create(self, user: CreateUserInput):
        try:
            await BaseUser.create_user(username=user.username,
                                       password=user.password,
                                       email=user.email,
                                       active=True)
            return json({"status": True})
        except Exception as e:
            return json({"status": False, "message": str(e)})

    @auth(Authenticated)
    @get("/verify_default")
    async def verify_default(self, user: Optional[Identity]):
        return json({"status": True, "user": user.claims})

    @auth(Roles.ADMIN)
    @get("/verify_admin")
    async def verify_admin(self, user: Optional[Identity]):
        return json({"status": True, "user": user.claims})

    @auth(Roles.SUPERADMIN)
    @get("/verify_superadmin")
    async def verify_superadmin(self, user: Optional[Identity]):
        return json({"status": True, "user": user.claims})