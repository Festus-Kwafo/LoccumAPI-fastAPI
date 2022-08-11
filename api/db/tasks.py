# from fastapi import FastAPI
# from databases import Database
# from api.core.config import DATABASE_URL
# import logging

from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from sqlalchemy import event
from sqlalchemy import select
from api.core.config import DATABASE_URL

some_engine = create_engine(DATABASE_URL)

@event.listens_for(some_engine, "engine_connect")
def ping_connection(connection, branch):
    if branch:
        # "branch" refers to a sub-connection of a connection,
        # we don't want to bother pinging on these.
        return

    # turn off "close with result".  This flag is only used with
    # "connectionless" execution, otherwise will be False in any case
    save_should_close_with_result = connection.should_close_with_result
    connection.should_close_with_result = False

    try:
        # run a SELECT 1.   use a core select() so that
        # the SELECT of a scalar value without a table is
        # appropriately formatted for the backend
        connection.scalar(select(1))
    except exc.DBAPIError as err:
        # catch SQLAlchemy's DBAPIError, which is a wrapper
        # for the DBAPI's exception.  It includes a .connection_invalidated
        # attribute which specifies if this connection is a "disconnect"
        # condition, which is based on inspection of the original exception
        # by the dialect in use.
        if err.connection_invalidated:
            # run the same SELECT again - the connection will re-validate
            # itself and establish a new connection.  The disconnect detection
            # here also causes the whole connection pool to be invalidated
            # so that all stale connections are discarded.
            connection.scalar(select(1))
        else:
            raise
    finally:
        # restore "close with result"
        connection.should_close_with_result = save_should_close_with_result

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=some_engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# logger = logging.getLogger(__name__)


# async def connect_to_db(app: FastAPI) -> None:
#     database = Database(DATABASE_URL, min_size=2, max_size=10)  # these can be configured in config as well

#     try:
#         await database.connect()
#         app.state._db = database
        
#     except Exception as e:
#         logger.warn("--- DB CONNECTION ERROR ---")
#         logger.warn(e)
#         logger.warn("--- DB CONNECTION ERROR ---")


# async def close_db_connection(app: FastAPI) -> None:
#     try:
#         await app.state._db.disconnect()
#     except Exception as e:
#         logger.warn("--- DB DISCONNECT ERROR ---")
#         logger.warn(e)
#         logger.warn("--- DB DISCONNECT ERROR ---")

