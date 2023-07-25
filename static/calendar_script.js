document.addEventListener('DOMContentLoaded', function () {
  var eventInfo;
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
      eventInfo = info;
      // Create the options box
      var optionsContainer = document.getElementById('optionsContainer');
      optionsContainer.innerHTML = ''; // Clear any previous content

      var editButton = document.createElement('button');
      editButton.textContent = 'Edit';
      editButton.addEventListener('click', function () {
        // Edit the event
        showEditForm(info.event);
        // Hide the options box after clicking "Edit"
        optionsContainer.style.display = 'none';
      });

      var deleteButton = document.createElement('button');
      deleteButton.textContent = 'Delete';
      deleteButton.addEventListener('click', function () {
        // Inside the eventClick function, add this line to make 'info' available in the scope
        var eventToDelete = calendar.getEventById(info.event.id);

        // Delete the event from the calendar
        console.log('Event ID to be deleted:', eventToDelete.id); // Add this line to check the event ID
        eventToDelete.remove();

        // Check if the event has a valid ID before making the DELETE request
        if (eventToDelete.id) {
          // Make a DELETE request to the server to remove the event
          fetch('/delete_event', {
            method: 'DELETE',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: eventToDelete.id }) // Pass the event ID in the request body
          })
            .then(response => response.json())
            .then(data => {
              console.log('Response from server:', data); // Add this line to see the response from the server
              console.log('Event deleted successfully:', data);
            })
            .catch(error => console.error('Error deleting event:', error));
        } else {
          console.error('Event ID is missing or invalid.');
        }

        // Hide the options box after clicking "Delete"
        optionsContainer.style.display = 'none';
      });

      // Append the buttons to the options container
      optionsContainer.appendChild(editButton);
      optionsContainer.appendChild(deleteButton);

      // Show the options box
      optionsContainer.style.display = 'block';
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

  // Function to show the event editing form when an event is clicked
  function showEditForm(event) {
    // Set the current event data in the form fields
    document.getElementById('editEventTitle').value = event.title;
    document.getElementById('editEventStartDate').value = event.start;
    document.getElementById('editEventStartTime').value = event.startStr.slice(11, 16);
    document.getElementById('editEventEndDate').value = event.end;
    document.getElementById('editEventEndTime').value = event.endStr.slice(11, 16);

    // Show the edit event form
    document.getElementById('editEventForm').style.display = 'block';
  }


  // Get the "Save" button element from the edit event form
  var editEventSaveButton = document.getElementById('editEventButton');

  // Add an event listener to the "Save" button
  editEventSaveButton.addEventListener('click', function () {
    // Get the updated values from the edit event form
    var updatedTitle = document.getElementById('editEventTitle').value;
    var updatedStartDate = document.getElementById('editEventStartDate').value;
    var updatedStartTime = document.getElementById('editEventStartTime').value;
    var updatedEndDate = document.getElementById('editEventEndDate').value;
    var updatedEndTime = document.getElementById('editEventEndTime').value;

    // Check if the user entered valid title, date, and time
    if (updatedTitle && updatedStartDate && updatedStartTime && updatedEndDate && updatedEndTime) {
      // Combine start date and time into a single string in ISO format
      var updatedStartDateTime = new Date(updatedStartDate + 'T' + updatedStartTime + ':00').toISOString();

      // Combine end date and time into a single string in ISO format
      var updatedEndDateTime = new Date(updatedEndDate + 'T' + updatedEndTime + ':00').toISOString();

      // Update the event on the calendar
      eventInfo.event.setProp('title', updatedTitle);
      eventInfo.event.setStart(updatedStartDateTime);
      eventInfo.event.setEnd(updatedEndDateTime);

      // Hide the edit event form after saving
      document.getElementById('editEventForm').style.display = 'none';

      // Send the updated event data to the server using a POST request
      var updatedEvent = {
        id: eventInfo.event.id,
        title: updatedTitle,
        start: updatedStartDateTime,
        end: updatedEndDateTime
      };

      fetch('/update_event', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(updatedEvent)
      })
        .then(response => response.json())
        .then(data => {
          if (data.message === 'Event data is incomplete') {
            console.error('Event data is incomplete. The server did not update the event.');
          } else {
            // Update the event on the calendar with the updated data received from the server
            eventInfo.event.setProp('title', data.updatedEvent.title);
            eventInfo.event.setStart(data.updatedEvent.start);
            eventInfo.event.setEnd(data.updatedEvent.end);
    
            console.log('Event updated successfully:', data);
          }
        })
        .catch(error => console.error('Error updating event:', error));
    } else {
      alert('Invalid input. Please fill in all fields.');
    }
  });
});
