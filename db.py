from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Instantiate Base
Base = declarative_base()

# Create the engine
engine = create_engine('sqlite:///bank.db')

# Create the tables
def create_tables():
    Base.metadata.create_all(engine)

# Drop all the tables
def drop_tables():
    Base.metadata.drop_all(engine)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get a session
def get_session():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()
