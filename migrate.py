from os import environ
from pathlib import Path

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, inspect, text


def migrate():
    engine = create_engine(environ["DATABASE_URL"])
    config = Config()
    config.set_main_option("script_location", str(Path(__file__).with_name("migrations")))

    with engine.begin() as connection:
        connection.execute(text("SELECT pg_advisory_xact_lock(6006)"))
        config.attributes["connection"] = connection
        tables = set(inspect(connection).get_table_names())
        if "alembic_version" not in tables and {"links", "link_events"} <= tables:
            command.stamp(config, "0001")
        command.upgrade(config, "head")


if __name__ == "__main__":
    migrate()
