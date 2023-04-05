from piccolo.engine import engine_finder

from blacksheep.server import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info
from auth.auth import AdminPolicy, AuthHandler, SuperAdminPolicy
from auth.data import Authenticated
from auth.jwt import JsonWebToken

import apps

from blacksheep.server.authorization import Policy
from guardpost.common import AuthenticatedRequirement

app = Application()


docs = OpenAPIHandler(info=Info(title="User API", version="0.0.1"))
docs.bind_app(app)


async def open_database_connection_pool(application):
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("无法连接到数据库, 请检查数据库连接是否正常")


async def close_database_connection_pool(application):
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("关闭数据库连接失败, 请检查数据库连接是否正常")


app.on_start += open_database_connection_pool
app.on_stop += close_database_connection_pool
app.services.add_instance(JsonWebToken())
provider = app.services.build_provider()
app.use_authentication().add(AuthHandler(jwt=provider.get(JsonWebToken)))
app.use_authorization().add(Policy(Authenticated,
                                   AuthenticatedRequirement())).add(
                                       AdminPolicy()).add(SuperAdminPolicy())
