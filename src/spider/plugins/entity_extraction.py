import asyncio
import logging
import spacy
from sqlalchemy import create_engine, Column, String, JSON, MetaData, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from spider.config import config
from spider.plugin import Plugin

# Set up the database engine and metadata.
engine = create_engine(config['database']['url'], echo=False)
metadata = MetaData()
entities_table = Table(
    'entities', metadata,
    Column('url', String, primary_key=True),
    Column('entities', JSON, nullable=False)
)
metadata.create_all(engine)

class EntityExtractionPlugin(Plugin):
    def __init__(self):
        # Load spaCy's small English model.
        self.nlp = spacy.load("en_core_web_sm")
        self.engine = engine

    async def should_run(self, url: str, content: str) -> bool:
        return True

    async def process(self, url: str, content: str) -> str:
        """
        Extract named entities from the content using spaCy and store them in the database.
        Synchronous database operations are run in a separate thread for efficiency.
        """
        def sync_process():
            try:
                doc = self.nlp(content)
                extracted_entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
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

        return await asyncio.to_thread(sync_process)
