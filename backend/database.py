import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Date, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for ORM models
Base = declarative_base()

# Create metadata object for raw SQL operations
metadata = MetaData()

# Define tables using metadata for raw SQL operations
reservations = Table(
    "reservations",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("reservation_number", String(50), unique=True, index=True),
    Column("date", Date),
    Column("status", String(50)),
    Column("customer_name", String(100)),
    Column("customer_email", String(100)),
)

archived_reservations = Table(
    "archived_reservations",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("reservation_number", String(50), unique=True, index=True),
    Column("date", Date),
    Column("status", String(50)),
    Column("customer_name", String(100)),
    Column("customer_email", String(100)),
)

# Define ORM models
class Reservation(Base):
    __tablename__ = "reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    reservation_number = Column(String(50), unique=True, index=True)
    date = Column(Date)
    status = Column(String(50))
    customer_name = Column(String(100))
    customer_email = Column(String(100))

class ArchivedReservation(Base):
    __tablename__ = "archived_reservations"
    
    id = Column(Integer, primary_key=True, index=True)
    reservation_number = Column(String(50), unique=True, index=True)
    date = Column(Date)
    status = Column(String(50))
    customer_name = Column(String(100))
    customer_email = Column(String(100))

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create tables if they don't exist
def create_tables():
    Base.metadata.create_all(bind=engine)
