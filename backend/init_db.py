import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta
from database import Base, Reservation, ArchivedReservation

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def init_db():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Check if there are already records in the reservations table
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM reservations"))
        count = result.scalar()
        
        if count == 0:
            print("No records found in reservations table. Adding sample data...")
            # Add sample data
            today = datetime.now().date()
            
            sample_data = [
                {
                    "reservation_number": "RES001",
                    "date": today,
                    "status": "Confirmed",
                    "customer_name": "John Doe",
                    "customer_email": "john.doe@example.com"
                },
                {
                    "reservation_number": "RES002",
                    "date": today - timedelta(days=1),
                    "status": "Confirmed",
                    "customer_name": "Jane Smith",
                    "customer_email": "jane.smith@example.com"
                },
                {
                    "reservation_number": "RES003",
                    "date": today - timedelta(days=2),
                    "status": "Cancelled",
                    "customer_name": "Bob Johnson",
                    "customer_email": "bob.johnson@example.com"
                },
                {
                    "reservation_number": "RES004",
                    "date": today + timedelta(days=1),
                    "status": "Pending",
                    "customer_name": "Alice Brown",
                    "customer_email": "alice.brown@example.com"
                },
                {
                    "reservation_number": "RES005",
                    "date": today + timedelta(days=2),
                    "status": "Confirmed",
                    "customer_name": "Charlie Wilson",
                    "customer_email": "charlie.wilson@example.com"
                }
            ]
            
            # Insert sample data using SQLAlchemy ORM
            from sqlalchemy.orm import sessionmaker
            SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
            db = SessionLocal()
            
            try:
                for data in sample_data:
                    reservation = Reservation(
                        reservation_number=data["reservation_number"],
                        date=data["date"],
                        status=data["status"],
                        customer_name=data["customer_name"],
                        customer_email=data["customer_email"]
                    )
                    db.add(reservation)
                
                db.commit()
                print("Sample data added successfully!")
            except Exception as e:
                db.rollback()
                print(f"Error adding sample data: {str(e)}")
            finally:
                db.close()
        else:
            print(f"Found {count} existing records in reservations table. Skipping sample data insertion.")

if __name__ == "__main__":
    init_db()
