import os
from piccolo.engine.postgres import PostgresEngine

from piccolo.conf.apps import AppRegistry

DB = PostgresEngine(
    config={
        "database": os.environ.get("DATABASE_NAME", "test"),
        "user": os.environ.get("DATEBASE_USER", "postgres"),
        "password": os.environ.get("DATEBASE_PASSWORD", "postgres"),
        "host": os.environ.get("DATEBASE_HOST", "localhost"),
        "port": 5432,
    })

APP_REGISTRY = AppRegistry(
    apps=["apps.baseuser.piccolo_app", "piccolo.apps.user.piccolo_app"])
