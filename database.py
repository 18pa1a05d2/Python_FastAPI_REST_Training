from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

#db_url="postgresql+psycopg2://postgres:Maha@123@localhost:5432/local"

db_url = URL.create(
    drivername="postgresql+psycopg2",
    username="postgres",
    password="Maha@123",
    host="localhost",
    port=5432,
    database="mahalakshmiputti"
)
engine = create_engine(db_url)
session = sessionmaker(engine, autoflush=False, autocommit=False)