from dataclasses import dataclass

from blacksheep.server.controllers import APIController, get, post
from blacksheep.server.bindings import FromJSON, FromServices, RequestUser
from blacksheep.server.authorization import auth
from piccolo.apps.user.tables import BaseUser
from utils.responses import json
from auth.jwt import JsonWebToken
from auth.data import Authenticated, JWTPayload, Roles


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

    @post("/login")
    async def login(self, input: FromJSON[UserInput], jwt: FromServices[JsonWebToken]):
        login = input.value
        if not (
            id := await BaseUser.login(username=login.username, password=login.password)
        ):
            return json({"status": False, "message": "Invalid username or password"})
        user: BaseUser = await BaseUser.objects().get(BaseUser.id == id)
        return json(
            {
                "status": True,
                "token": jwt.value.creact_jwt_token(
                    JWTPayload(
                        id=id,
                        name=user.username,
                        email=user.email,
                        is_superuser=user.superuser,
                        is_admin=user.admin,
                    )
                ),
            }
        )

    @post("/create_user")
    async def create(self, input: FromJSON[CreateUserInput]):
        user = input.value
        if await BaseUser.exists().where(BaseUser.username == user.username):
            return json({"status": False, "message": "用户名已存在"})

        if await BaseUser.exists().where(BaseUser.email == user.email):
            return json({"status": False, "message": "该邮箱已被注册过"})

        try:
            await BaseUser.create_user(
                username=user.username,
                password=user.password,
                email=user.email,
                active=True,
            )
            return json({"status": True})
        except ValueError as e:
            return json({"status": False, "message": e})

    @auth(Authenticated)
    @get("/verify_default")
    async def verify_default(self, user: RequestUser):
        return json({"status": True, "user": user.value.claims})

    @auth(Roles.ADMIN)
    @get("/verify_admin")
    async def verify_admin(self, user: RequestUser):
        return json({"status": True, "user": user.value.claims})

    @auth(Roles.SUPERADMIN)
    @get("/verify_superadmin")
    async def verify_superadmin(self, user: RequestUser):
        return json({"status": True, "user": user.value.claims})
