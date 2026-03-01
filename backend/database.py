from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# UPDATE THESE WITH YOUR ACTUAL CREDENTIALS
DATABASE_URL = "postgresql://postgres:Rusha%40057@localhost:5432/medicare_db"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()