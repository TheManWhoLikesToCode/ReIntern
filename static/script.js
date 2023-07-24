document.addEventListener('DOMContentLoaded', function () {
  var calendarEl = document.getElementById('calendar');

  // Initialize FullCalendar
  var calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: ['dayGrid', 'interaction'], // Required plugins
    header: {
      left: 'prev,next today', // Navigation buttons
      center: 'title', // Display the current month/year as the title
      right: 'dayGridMonth,dayGridWeek,dayGridDay', // Display different views (month, week, day)
    },
    events: [
    ],
    timeZone: 'local', // Set the time zone (change to your specific time zone)
  });

  // Render the calendar
  calendar.render();

  // Add event listener to the summaryForm submit button
  document.getElementById('summaryForm').addEventListener('submit', function (event) {
    event.preventDefault();
    submitSummary();
  });
});

function submitSummary() {
  var summary = document.getElementById('dailySummary').value;

  // Input validation
  if (!summary) {
    alert('Please enter a summary.');
    return;
  }

  // Convert the summary to a JSON string
  var summaryJson = JSON.stringify({
    summary: summary,
  });

  console.log('Sending JSON: ', summaryJson);

  fetch('/home', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: summaryJson,
  })
    .then((response) => {
      // Log the response
      console.log('Response received: ', response);

      // Read the response as JSON
      return response.json();
    })
    .then((data) => {
      // Log the response data
      console.log('Response data: ', data);

      // Update the summaryResult paragraph with the response data
      document.getElementById('summaryResult').innerText = data.brag_sheet_bullets;
    })
    .catch((error) => console.error(error));
}
