from sqlalchemy import create_engine, Table, MetaData
from datetime import date, timedelta
import os
import random
import string
from dotenv import load_dotenv

load_dotenv()

db_link = os.getenv("DATABASE_URL")

my_engine = create_engine(db_link)
my_metadata = MetaData()

my_reservations = Table(
    "reservations", 
    my_metadata,
    autoload_with=my_engine
)

def make_booking_number(start_text="RES"):
    random_numbers = ''.join(random.choices(string.digits, k=3))
    return f"{start_text}{random_numbers}"

def make_random_name():
    first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda", 
                  "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica", 
                  "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa", 
                  "Matthew", "Betty", "Anthony", "Dorothy", "Mark", "Sandra", "Donald", "Ashley"]
    
    last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", 
                 "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", 
                 "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee", 
                 "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez"]
    
    return f"{random.choice(first_names)} {random.choice(last_names)}"

def make_email(name):
    email_endings = ["gmail.com", "yahoo.com", "hotmail.com", "outlook.com", "icloud.com", "aol.com", "protonmail.com"]
    name_bits = name.lower().split()
    user_part = f"{name_bits[0]}.{name_bits[1]}"
    return f"{user_part}@{random.choice(email_endings)}"

def pick_booking_status():
    possible_statuses = ["Confirmed", "Pending", "Cancelled"]
    chances = [0.7, 0.2, 0.1]
    return random.choices(possible_statuses, weights=chances, k=1)[0]

my_connection = my_engine.connect()

right_now = date.today()
all_bookings = []

for i in range(1, 31):
    if i % 2 == 0:
        booking_day = right_now + timedelta(days=i//2)
    else:
        booking_day = right_now - timedelta(days=(i+1)//2)
    
    person_name = make_random_name()
    person_email = make_email(person_name)
    
    booking_info = {
        "reservation_number": make_booking_number(),
        "date": booking_day,
        "status": pick_booking_status(),
        "customer_name": person_name,
        "customer_email": person_email
    }
    
    all_bookings.append(booking_info)

for one_booking in all_bookings:
    my_connection.execute(my_reservations.insert().values(**one_booking))

my_connection.commit()

print(f"Added {len(all_bookings)} new bookings to the database.")
print("Here are some of the bookings:")
for i, booking in enumerate(all_bookings[:5]):
    print(f"  - {booking['reservation_number']}: {booking['date']} ({booking['status']}) - {booking['customer_name']}")

print(f"... and {len(all_bookings) - 5} more.")

my_connection.close()
