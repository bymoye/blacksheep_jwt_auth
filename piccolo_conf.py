from piccolo.engine.postgres import PostgresEngine

from piccolo.conf.apps import AppRegistry

DB = PostgresEngine(
    config={
        "database": "test",
        "user": "postgres",
        "password": "postgres",
        "host": "localhost",
        "port": 5432,
    })

APP_REGISTRY = AppRegistry(
    apps=["apps.baseuser.piccolo_app", "piccolo.apps.user.piccolo_app"])
