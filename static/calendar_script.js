document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    events: [], // Initialize events as an empty array
    eventClick: function (info) {
      alert('Event: ' + info.event.title);
      alert('Coordinates: ' + info.jsEvent.pageX + ',' + info.jsEvent.pageY);
      alert('View: ' + info.view.type);
      // change the border color just for fun
      info.el.style.borderColor = 'red';
    }
  });

  // Fetch events associated with the logged-in user
  fetch('/get_events')
    .then(response => response.json())  // Parse the JSON response
    .then(data => {
      // The data variable should now be an array of event objects
      const events = data;

      // Add the fetched events to the calendar
      calendar.addEventSource(events);
      calendar.render(); // Render the calendar after adding the events
    })
    .catch(error => console.error('Error fetching events:', error));

  // Get the "Add Event" button element
  var addEventButton = document.getElementById('addEventButton');
  addEventButton.addEventListener('click', function () {
    // Get the values from the input fields
    var title = document.getElementById('eventTitle').value;
    var date = document.getElementById('eventDate').value;
    var time = document.getElementById('eventTime').value;

    // Check if the user entered valid title, date, and time
    if (title && date && time) {
      // Combine date and time into a single string in ISO 8601 format (e.g., "2023-07-25T14:30:00")
      var dateTime = date + 'T' + time;

      var event = {
        title: title,
        start: dateTime,
      };

      // Add the event to the calendar and refresh
      calendar.addEvent(event);

      // Clear the input fields after adding the event
      document.getElementById('eventTitle').value = '';
      document.getElementById('eventDate').value = '';
      document.getElementById('eventTime').value = '';

      // Store the event on the server-side using a POST request
      fetch('/add_event', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(event)
      })
      .then(response => response.json())
      .then(data => {
        console.log('Event added successfully:', data);
      })
      .catch(error => console.error('Error adding event:', error));
    } else {
      alert('Invalid input. Please fill in all fields.');
    }
  });
});
