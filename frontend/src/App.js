import React, { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

function App() {
  const [date, setDate] = useState('');
  const [reservationNumber, setReservationNumber] = useState('');
  const [responseMessage, setResponseMessage] = useState('');
  const [status, setStatus] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!date && !reservationNumber) {
      setResponseMessage('Please enter either a date or a reservation number');
      setIsError(true);
      return;
    }
    
    setIsLoading(true);
    setResponseMessage('');
    setStatus('');
    setIsError(false);
    
    try {
      const response = await axios.post(`${API_BASE_URL}/api/archive-reservation`, {
        date: date || null,
        reservation_number: reservationNumber || null
      });
      
      setResponseMessage(response.data.message);
      setStatus(response.data.status);
      setIsError(!response.data.status);
    } catch (error) {
      console.error('Error details:', error);
      setResponseMessage(error.response?.data?.detail || 'An error occurred while processing your request');
      setIsError(true);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto bg-white rounded-lg shadow-md overflow-hidden">
        <div className="px-4 py-5 sm:p-6">
          <h1 className="text-2xl font-bold text-gray-900 text-center mb-2">
            Reservation Archive System
          </h1>
          <p className="text-center text-gray-600 mb-6">
            Enter <strong>either</strong> a date <strong>or</strong> a reservation number below
          </p>
          <p className="text-center text-gray-500 mb-4 text-sm">
            <span className="block">• If you enter a <strong>date</strong>, all reservations on or before that date will be archived.</span>
            <span className="block">• If you enter a <strong>reservation number</strong>, only that specific reservation will be archived.</span>
          </p>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label htmlFor="date" className="block text-sm font-medium text-gray-700">
                Archive Date (all reservations on or before this date)
              </label>
              <div className="mt-1">
                <input
                  type="date"
                  id="date"
                  name="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                />
              </div>
            </div>

            <div>
              <label htmlFor="reservation-number" className="block text-sm font-medium text-gray-700">
                Reservation Number
              </label>
              <div className="mt-1">
                <input
                  type="text"
                  id="reservation-number"
                  name="reservation-number"
                  value={reservationNumber}
                  onChange={(e) => setReservationNumber(e.target.value)}
                  placeholder="e.g. RES001"
                  className="shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md p-2 border"
                />
              </div>
            </div>

            <div className="text-center">
              <button
                type="submit"
                disabled={isLoading}
                className={`inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white ${
                  isLoading ? 'bg-indigo-300' : 'bg-indigo-600 hover:bg-indigo-700'
                } focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
              >
                {isLoading ? 'Processing...' : 'Submit'}
              </button>
            </div>
          </form>
          
          {responseMessage && (
            <div className={`mt-6 p-4 rounded-md ${isError ? 'bg-red-50 text-red-700' : status === 'already_archived' ? 'bg-yellow-50 text-yellow-700' : 'bg-green-50 text-green-700'}`}>
              <p>{responseMessage}</p>
              {status && status !== 'already_archived' && (
                <div className="mt-2">
                  <p className="font-semibold">Reservation Status: <span className="font-normal">{status}</span></p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
