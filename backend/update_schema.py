from sqlalchemy import create_engine, MetaData, Table, Column, String
import os
from dotenv import load_dotenv

load_dotenv()

my_db = os.getenv("DATABASE_URL")

my_engine = create_engine(my_db)
my_tables = MetaData()

my_tables.reflect(bind=my_engine)

bookings = my_tables.tables['reservations']
old_bookings = my_tables.tables['archived_reservations']

if 'customer_email' not in bookings.c:
    print("Adding email column to bookings table...")
    with my_engine.begin() as db_conn:
        db_conn.execute(f"ALTER TABLE reservations ADD COLUMN customer_email VARCHAR(100)")
    print("Added email column to bookings table.")
else:
    print("email column already exists in bookings table.")

if 'customer_email' not in old_bookings.c:
    print("Adding email column to old bookings table...")
    with my_engine.begin() as db_conn:
        db_conn.execute(f"ALTER TABLE archived_reservations ADD COLUMN customer_email VARCHAR(100)")
    print("Added email column to old bookings table.")
else:
    print("email column already exists in old bookings table.")

print("Database updated!!")
