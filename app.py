from piccolo_admin.endpoints import create_admin
from piccolo.engine import engine_finder

from blacksheep.server import Application
from blacksheep.server.openapi.v3 import OpenAPIHandler
from openapidocs.v3 import Info
from auth.auth import AdminPolicy, AuthHandler
from auth.data import Authenticated
from auth.jwt import JsonWebToken
from config import Gconfig

from home.endpoints import Home
from baseuser.endpoints import BaseUser
from home.piccolo_app import APP_CONFIG
from blacksheep.server.authorization import Policy
from guardpost.common import AuthenticatedRequirement
app = Application()

app.mount(
    "/admin/",
    create_admin(
        tables=APP_CONFIG.table_classes,
        # Required when running under HTTPS:
        # allowed_hosts=['my_site.com']
    ),
)

docs = OpenAPIHandler(info=Info(title="Example API", version="0.0.1"))
docs.bind_app(app)

# app.router.add_post("/login", jwt_login)

async def open_database_connection_pool(application):
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")


async def close_database_connection_pool(application):
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")


app.on_start += open_database_connection_pool
app.on_stop += close_database_connection_pool
app.services.add_instance(JsonWebToken(Gconfig()))
provider = app.services.build_provider()
app.use_authentication().add(AuthHandler(jwt=provider.get(JsonWebToken)))
app.use_authorization().add(
    Policy(Authenticated, AuthenticatedRequirement())).add(AdminPolicy())