'use client';
// Calendar.js
import React, { useEffect } from 'react';
import { useGoogleCalendar } from '@/services/GoogleCalendarContext'; // Adjust path as necessary

const Calendar = () => {
  const { calendarEvents, fetchCalendarEvents, googleLogin } = useGoogleCalendar();

  useEffect(() => {
    fetchCalendarEvents();
  }, [fetchCalendarEvents]);

  return (
    <div className="calendar-container">
      <button onClick={() => googleLogin()}>Login with Google</button>
      <h2>Upcoming Events</h2>
      <ul>
        {calendarEvents.map(event => (
          <li key={event.id}>
            <h3>{event.summary}</h3>
            <p>{new Date(event.start.dateTime).toLocaleString()} - {new Date(event.end.dateTime).toLocaleString()}</p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Calendar;
