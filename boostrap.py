import logging

from sqlalchemy import select

from data_sources.symbols.fetch_all_symbols import fetch_all_symbols
from database.connector import DatabaseConnector
from database.models import *

logger = logging.getLogger(__name__)


async def bootstrap(db_connector: DatabaseConnector):
    logger.info("bootstrapping database...")
    await db_connector.init_db()
    await _sync_db_symbols(db_connector)


async def _sync_db_symbols(db_connector: DatabaseConnector):
    # fetch all the symbols from the data sources, and add the ones that are missing from the Equities table
    symbol_list = set(fetch_all_symbols())
    async with db_connector as session:
        # get all the symbols that are already in the database
        select_stmt = select(Equity.symbol)
        result = await session.execute(select_stmt)
        existing_symbols = set([row[0] for row in result.all()])
        new_symbols = symbol_list - existing_symbols
        if len(new_symbols) > 0:
            async with session.begin():
                logger.info(f"found {len(new_symbols)} new symbols")
                session.add_all([Equity(symbol=symbol) for symbol in new_symbols])
        else:
            logger.info("no new symbols found")
