from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from typing import Optional
from datetime import date as date_type, datetime
from database import get_db, create_tables, Reservation, ArchivedReservation
from pydantic import BaseModel, validator

my_app = FastAPI()

my_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@my_app.on_event("startup")
async def start_my_app():
    create_tables()

class BookingRequest(BaseModel):
    date: Optional[str] = None
    reservation_number: Optional[str] = None
    
    @validator('date', 'reservation_number')
    def check_empty(cls, v):
        if v == "":
            return None
        return v

class BookingResponse(BaseModel):
    message: str
    status: Optional[str] = None

@my_app.post("/api/archive-reservation", response_model=BookingResponse)
async def save_old_bookings(request: BookingRequest, db: Session = Depends(get_db)):
    try:
        if not request.date and not request.reservation_number:
            raise HTTPException(status_code=400, detail="Either date or reservation number must be provided")
        
        if request.reservation_number:
            old_booking_search = select(ArchivedReservation).where(
                ArchivedReservation.reservation_number == request.reservation_number
            )
            search_result = db.execute(old_booking_search)
            old_booking = search_result.scalar_one_or_none()
            
            if old_booking:
                return {
                    "message": f"Reservation {request.reservation_number} has already been archived.",
                    "status": "already_archived"
                }
        
        my_search = select(Reservation)
        
        if request.date:
            try:
                user_date = datetime.strptime(request.date, "%Y-%m-%d").date()
                my_search = my_search.where(Reservation.date <= user_date)
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        if request.reservation_number:
            my_search = my_search.where(Reservation.reservation_number == request.reservation_number)
        
        result = db.execute(my_search)
        bookings_to_save = result.scalars().all()
        
        if not bookings_to_save:
            return {"message": "No matching reservations found", "status": None}
        
        saved_count = 0
        first_date = None
        last_date = None
        
        for booking in bookings_to_save:
            old_booking = ArchivedReservation(
                reservation_number=booking.reservation_number,
                date=booking.date,
                status=booking.status,
                customer_name=booking.customer_name,
                customer_email=booking.customer_email if hasattr(booking, 'customer_email') else None
            )
            db.add(old_booking)
            
            if first_date is None or booking.date < first_date:
                first_date = booking.date
            if last_date is None or booking.date > last_date:
                last_date = booking.date
            
            db.delete(booking)
            saved_count += 1
        
        db.commit()
        
        if request.reservation_number:
            msg = f"Reservation {request.reservation_number} has been archived successfully."
        else:
            date_text = ""
            if first_date == last_date:
                date_text = f"on {first_date}"
            else:
                date_text = f"from {first_date} to {last_date}"
            
            msg = f"All {saved_count} reservations {date_text} have been archived successfully."
        
        return {
            "message": msg,
            "status": "archived"
        }
    
    except HTTPException as error:
        db.rollback()
        raise error
    except Exception as oops:
        db.rollback()
        import traceback
        error_details = traceback.format_exc()
        print(f"Error in save_old_bookings: {str(oops)}")
        print(f"Error details: {error_details}")
        return {"message": f"Error: {str(oops)}", "status": None}

@my_app.get("/api/health")
async def is_working():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:my_app", host="0.0.0.0", port=8000, reload=True)
