from DataStats.app.database.database_object import DatabaseManager
from DataStats.app.core.config import (
    DB_NAME, DB_HOST,
    DB_PASSWORD, DB_USER
)

db_manager = DatabaseManager(
        host=DB_HOST,
        username=DB_USER,
        password=DB_PASSWORD,
        database_name=DB_NAME
    )


