import json
from collections import Counter
from sqlalchemy import create_engine, select, MetaData, Table
from sqlalchemy.orm import sessionmaker
from spider.config import config

engine = create_engine(config['database']['url'], echo=False)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# Create a MetaData instance and reflect the entities table.
metadata = MetaData()
entities_table = Table(
    'entities',
    metadata,
    autoload_with=engine
)

def analyze_entities():
    """
    Query the entities table to compute the frequency of each entity label.
    """
    query = select(entities_table.c.entities)
    results = session.execute(query).fetchall()

    # Create a counter for entity labels.
    label_counter = Counter()
    for row in results:
        # Each row's 'entities' column is expected to be a JSON value (a list of entity dicts).
        entities = row[0]
        # If entities are stored as a JSON string, load them.
        if isinstance(entities, str):
            entities = json.loads(entities)
        for entity in entities:
            label = entity.get('label')
            if label:
                label_counter[label] += 1

    print("Top 10 entity labels:")
    for label, count in label_counter.most_common(10):
        print(f"{label}: {count}")

if __name__ == '__main__':
    analyze_entities()
