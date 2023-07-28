from boostrap import bootstrap
from database.connector import DatabaseConnector


async def main():
    db = DatabaseConnector()
    await bootstrap(db)
    