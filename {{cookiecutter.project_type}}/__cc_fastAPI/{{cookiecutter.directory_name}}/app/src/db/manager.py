# database manager functions to interact with database
from typing import Generator

# from pyramid.config import Configurator
from sqlalchemy import MetaData
from app.src.db.engine import engine, SessionLocal
from app.src.logger import logger
from app.src.db import base


# get engine sqlalchemy session
# you can use the session in the scripts by doing
# session = get_session()
# next(session).query(....)
def get_session() -> Generator:
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()


# create table
def create_tables() -> bool:
    # Database Engine
    # config = Configurator()
    # config.scan("app.src.models")  # search for all the tables
    # metadata = MetaData()
    try:
        # for table in objects:
        #     new_table = table
        #     logger.debug(f"Creating new table: {new_table}")
        base.Base.metadata.create_all(engine)
        return True
    except Exception as message:
        logger.error("Impossible to create the tables")
        logger.exception(message)
        raise Exception(message)


# drop all tables in the db
def drop_all_tables() -> bool:
    try:
        base.Base.metadata.drop_all(engine)
        return True
    except Exception as message:
        logger.error("Impossible to drop all the tables in the db")
        logger.exception(message)
        raise Exception(message)


# check table existing in the database
def check_table() -> dict:
    try:
        tables = base.Base.metadata.tables.keys()
        if tables:
            return tables
        else:
            logger.info("No tables existing in the database")
            return None
    except Exception as message:
        logger.error("Impossible to get the table names in the db")
        logger.exception(message)
        raise Exception(message)


# get tablename db schema
def get_table_schema(table_name: str) -> dict:
    try:
        # we use here the sqlalchemy metadata reflection
        # https://docs.sqlalchemy.org/en/14/core/reflection.html#reflecting-all-tables-at-once
        m = MetaData()
        m.reflect(engine)
        table_schema = {}
        for column in m.tables[table_name].c:
            table_schema[column.name.name] = column.name.type
        if table_schema:
            return table_schema
        else:
            logger.info(f"No columns existing in the table: {table_name}")
            return None
    except Exception as message:
        logger.error(f"Impossible to get the schema for the table: {table_name}")
        logger.exception(message)
        raise Exception(message)


# insert new table with data
def insert_data(your_object: object) -> bool:
    try:
        with SessionLocal.begin() as session:
            session.add(your_object)
            session.commit()
            session.refresh(your_object)
        return True
    except Exception as message:
        logger.error(
            f"Impossible to create the table for the object: {your_object.__class__.__name__}"
        )
        logger.exception(message)
        raise Exception(message)


# refresh the schema and data
def refresh_data(your_object: object) -> bool:
    try:
        with SessionLocal.begin() as session:
            session.refresh(your_object)
        return True
    except Exception as message:
        logger.error(
            f"Impossible to refresh the object: {your_object.__class__.__name__}"
        )
        logger.exception(message)
        raise Exception(message)


# delete an object
def delete_data(your_object: object) -> bool:
    try:
        with SessionLocal.begin() as session:
            session.delete(your_object)
            session.commit()
        return True
    except Exception as message:
        logger.error(
            f"Impossible to delete your object: {your_object.__class__.__name__}"
        )
        logger.exception(message)
        raise Exception(message)


# get info (select)
# get all (select *)
# update single row
# delete single row
# launch a query
