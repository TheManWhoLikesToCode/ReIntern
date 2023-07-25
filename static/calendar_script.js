document.addEventListener('DOMContentLoaded', function () {
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
    .then(response => response.json()) // Parse the JSON response
    .then(data => {
      // The data variable should now be an array of event objects
      const events = data;

      // Add the fetched events to the calendar
      calendar.addEventSource(events);
    })
    .catch(error => console.error('Error fetching events:', error));

  calendar.render();

  // Get the "Add Event" button element
  var addEventButton = document.getElementById('addEventButton');
  addEventButton.addEventListener('click', function () {
    // Get the values from the input fields
    var title = document.getElementById('eventTitle').value;
    var startDate = document.getElementById('eventDate').value;
    var startTime = document.getElementById('eventTime').value;
    var endDate = document.getElementById('eventEndDate').value;
    var endTime = document.getElementById('eventEndTime').value;

    // Check if the user entered valid title, date, and time
    if (title && startDate && startTime && endDate && endTime) {
      // Combine start date and time into a single string in ISO format
      var startDateTime = startDate + 'T' + startTime + ':00';

      // Combine end date and time into a single string in ISO format
      var endDateTime = endDate + 'T' + endTime + ':00';

      var event = {
        title: title,
        start: startDateTime,
        end: endDateTime
      };

      // Add the event to the calendar and refresh
      calendar.addEvent(event);
      calendar.render();

      // Clear the input fields after adding the event
      document.getElementById('eventTitle').value = '';
      document.getElementById('eventDate').value = '';
      document.getElementById('eventTime').value = '';
      document.getElementById('eventEndDate').value = '';
      document.getElementById('eventEndTime').value = '';

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
