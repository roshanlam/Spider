import logging
from sqlalchemy import create_engine, Column, String, Text, MetaData, Table, insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert as pg_insert
from spider.config import config

# Configure the engine and sessionmaker.
engine = create_engine(config['database']['url'], echo=False)
SessionLocal = sessionmaker(bind=engine)
metadata = MetaData()

pages_table = Table(
    'pages', metadata,
    Column('url', String, primary_key=True),
    Column('content', Text, nullable=False)
)

metadata.create_all(engine)

def save_page(url: str, content: str) -> None:
    """
    Save the crawled page content into the database.

    This function attempts to use PostgreSQL's ON CONFLICT clause to ignore duplicate inserts.
    If on_conflict_do_nothing is not available, it falls back to catching IntegrityError exceptions.

    :param url: The URL of the crawled page.
    :param content: The page content.
    """
    session = SessionLocal()
    try:
        stmt = pg_insert(pages_table).values(url=url, content=content)
        # Try to use on_conflict_do_nothing if available.
        try:
            stmt = stmt.on_conflict_do_nothing(index_elements=['url'])
        except AttributeError:
            logging.warning("on_conflict_do_nothing not available; will handle duplicates via IntegrityError")
        session.execute(stmt)
        session.commit()
        logging.info(f"Saved page: {url}")
    except IntegrityError:
        session.rollback()
        logging.info(f"Page {url} already exists. Skipping insertion.")
    except SQLAlchemyError as e:
        session.rollback()
        logging.error(f"Error saving page {url}: {e}")
    finally:
        session.close()
