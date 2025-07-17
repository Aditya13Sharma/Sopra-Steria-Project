# Reservation Archive System

A full-stack web application for filtering and archiving reservation records from a MySQL database.

## Project Structure

```
reservation-system/
├── backend/
│   ├── .env                  # Environment variables
│   ├── database.py           # Database models and connection
│   ├── init_db.py            # Database initialization script
│   ├── main.py               # FastAPI backend
│   └── requirements.txt      # Python dependencies
└── frontend/
    ├── public/
    │   └── index.html        # HTML template
    ├── src/
    │   ├── App.js            # Main React component
    │   ├── index.css         # CSS with Tailwind imports
    │   └── index.js          # React entry point
    ├── package.json          # Node.js dependencies
    ├── postcss.config.js     # PostCSS configuration
    └── tailwind.config.js    # Tailwind CSS configuration
```

## Setup Instructions

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```
   uvicorn main:my_app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required dependencies:
   ```
   npm install
   ```

3. Start the React development server:
   ```
   npm start
   ```

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Enter either a date or a reservation number:
   - If you enter a date, all reservations on or before that date will be archived
   - If you enter a reservation number, only that specific reservation will be archived
3. Click the Submit button
4. The system will move matching reservations from the `reservations` table to the `archived_reservations` table
5. A status message will be displayed indicating the result of the operation

## Database Configuration

The application connects to a MySQL database using the connection string specified in the `.env` file. Make sure your MySQL server is running and the database exists before starting the application.

## API Endpoints

- `POST /api/archive-reservation`: Archives reservations based on date or reservation number
- `GET /api/health`: Health check endpoint

## Technologies Used

- **Backend**: FastAPI, SQLAlchemy, PyMySQL
- **Frontend**: React, Tailwind CSS, Axios
- **Database**: MySQL
