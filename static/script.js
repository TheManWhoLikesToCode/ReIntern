window.onload = function () {
  document
    .getElementById("summaryForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      submitSummary();
    });
};

function submitSummary() {
  var summary = document.getElementById("dailySummary").value;

  // Input validation
  if (!summary) {
    alert("Please enter a summary.");
    return;
  }

  // Convert the summary to a JSON string
  var summaryJson = JSON.stringify({
    summary: summary,
  });

  console.log("Sending JSON: ", summaryJson);

  fetch("/home", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: summaryJson,
  })
    .then((response) => {
      // Log the response
      console.log("Response received: ", response);

      // Read the response as JSON
      return response.json();
    })
    .then((data) => {
      // Log the response data
      console.log("Response data: ", data);

      // Update the summaryResult paragraph with the response data
      document.getElementById("summaryResult").innerText =
        data.brag_sheet_bullets;
    })
    .catch((error) => console.error(error));
}
