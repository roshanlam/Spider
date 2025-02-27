import logging
import spacy
from sqlalchemy import create_engine, Column, String, JSON, MetaData, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from config import config
from plugin import Plugin

# Set up the database engine and metadata.
engine = create_engine(config['database']['url'], echo=False)
metadata = MetaData()

# Define a table to store extracted entities.
entities_table = Table(
    'entities', metadata,
    Column('url', String, primary_key=True),
    Column('entities', JSON, nullable=False)
)

metadata.create_all(engine)

class EntityExtractionPlugin(Plugin):
    """
    An advanced plugin that extracts named entities from crawled page content using spaCy,
    then stores the entities in a PostgreSQL table for later analysis.

    The plugin processes the HTML content, extracts entities with their labels, and performs
    an upsert operation into the 'entities' table.
    """
    def __init__(self):
        # Load spaCy's small English model for named entity recognition.
        self.nlp = spacy.load("en_core_web_sm")
        self.engine = engine

    def process(self, url: str, content: str) -> str:
        """
        Extract named entities from the page content and store them in the database.

        :param url: The URL of the crawled page.
        :param content: The HTML content of the page.
        :return: The original content (unmodified).
        """
        try:
            # Process the page content using spaCy.
            doc = self.nlp(content)
            # Extract entities: a list of dictionaries with 'text' and 'label'.
            extracted_entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]

            # Prepare an upsert statement using PostgreSQL dialect.
            stmt = pg_insert(entities_table).values(url=url, entities=extracted_entities)
            stmt = stmt.on_conflict_do_update(
                index_elements=['url'],
                set_={'entities': extracted_entities}
            )

            with self.engine.connect() as conn:
                conn.execute(stmt)
                conn.commit()

            logging.info(f"Extracted and stored entities for {url}")
        except SQLAlchemyError as db_err:
            logging.error(f"Database error storing entities for {url}: {db_err}")
        except Exception as e:
            logging.error(f"Error processing entities for {url}: {e}")
        return content
