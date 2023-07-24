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
      .then(response => response.json())
      .then(data => {
        // Add the fetched events to the calendar
        calendar.addEventSource(data);
      })
      .catch(error => console.error('Error fetching events:', error));
  
    calendar.render();
  
    // Get the "Add Event" button element
    var addEventButton = document.getElementById('addEventButton');
    addEventButton.addEventListener('click', function () {
      // Get the values from the input fields
      var title = document.getElementById('eventTitle').value;
      var date = document.getElementById('eventDate').value;
      var time = document.getElementById('eventTime').value;
  
      // Check if the user entered valid title, date, and time
      if (title && date && time) {
        // Combine date and time into a single string in MM/DD/YYYY HH:mm format
        var dateTime = date + ' ' + time;
  
        var event = {
          title: title,
          start: dateTime,
        };
  
        // Add the event to the calendar and refresh
        calendar.addEvent(event);
        calendar.render();
  
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
  