import logging
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, String, Text, MetaData, Table
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import SQLAlchemyError
from spider.config import config
from spider.plugin import Plugin

# Configure the database
engine = create_engine(config['database']['url'], echo=False)
metadata = MetaData()

# Define the titles table
titles_table = Table(
    'titles', metadata,
    Column('url', String, primary_key=True),
    Column('title', Text, nullable=True)
)

# Create the table if it doesn't exist
metadata.create_all(engine)

class TitleLoggerPlugin(Plugin):
    async def should_run(self, url: str, content: str) -> bool:
        return True

    async def process(self, url: str, content: str) -> str:
        """
        Extracts the <title> tag from the HTML content using BeautifulSoup (with lxml)
        and saves it to the database. Also logs the title if found.
        Returns the unmodified content.
        """
        try:
            soup = BeautifulSoup(content, 'lxml')
            title_tag = soup.find('title')
            title = title_tag.string.strip() if title_tag and title_tag.string else None

            if title:
                logging.info(f"Page Title for {url}: {title}")
                # Save to database to new table
                stmt = pg_insert(titles_table).values(
                    url=url,
                    title=title
                )
                stmt = stmt.on_conflict_do_update(
                    index_elements=['url'],
                    set_={'title': title}
                )
                with engine.connect() as conn:
                    conn.execute(stmt)
                    conn.commit()
                logging.info(f"Saved title to database for {url}")
            else:
                logging.info(f"No title found for {url}")
                # Save NULL title to database
                stmt = pg_insert(titles_table).values(
                    url=url,
                    title=None
                )
                stmt = stmt.on_conflict_do_update(
                    index_elements=['url'],
                    set_={'title': None}
                )
                with engine.connect() as conn:
                    conn.execute(stmt)
                    conn.commit()
                logging.info(f"Saved NULL title to database for {url}")

        except SQLAlchemyError as e:
            logging.error(f"Database error saving title for {url}: {e}")
        except Exception as e:
            logging.error(f"Error processing title for {url}: {e}")
        
        return content
