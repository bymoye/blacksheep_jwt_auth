from blacksheep.server.controllers import APIController,get,post
from dataclasses import dataclass
from blacksheep.server.authorization import auth
from blacksheep import  text, json
from auth.data import Authenticated
from config import Gconfig
@dataclass
class CreateFooInput:
    name: str
    nice: bool

class Roles:
    ADMIN = "ADMIN"

class Home(APIController):
    @classmethod
    def version(cls):
        return "v1"
    
    def greet(self):
        return "Hello World"

    @get("/")
    async def index(self):
        return text(self.greet())

    # @auth(Roles.ADMIN)
    @auth(Authenticated)
    @get("/foo")
    async def foo(self):
        return json({"id": 1, "name": "foo", "nice": True})

    @auth(Authenticated)
    @post("/foo")
    async def create_foo(self, foo: CreateFooInput):
        return json({"status": True})