from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

import time
import psycopg2
from psycopg2.extras import RealDictCursor

## ^^ FROM SQL documentation for working with SQLALCHEMY

## CONNECTING to postgres database driver
# Template for URL: "postgresql://username:password@ip-address/hostname/databasename"

# ENGINE is repsponsible for connection with postgres, dont hardcode the link

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base() ## Creating tables is basically extending this BASE class

# Dependency
# The session object is responsible for talking to the database.
# Every time you need to request database, call this function, ez
# For all following functions, whenev we need database, call instance of get_db, use methods, ez
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


# while True:

# ## DONT HARDCODE this login info, make functionality for logging in later
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#         password='Superbilloo1010$', cursor_factory=RealDictCursor)
#         cursor = conn.cursor() ## USING THIS OBJECT to execute SQL statements on our database from HERE
#         print("Connection to database was successful!")
#         break
#     except Exception as error:
#         print("Exception: connection to database has failed.")
#         print("Error: ", error)
#         time.sleep(2)

