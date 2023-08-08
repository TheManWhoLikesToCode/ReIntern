function generateEmail() {
  document.getElementById("loadingOverlay").style.display = "flex"; // Show overlay and spinner

  const summary = document.getElementById("emailContent").innerText;
  fetch("/generate_email", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ summary: summary }),
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((errorData) => {
          throw new Error(errorData.message);
        });
      }
      return response.json();
    })
    .then((data) => {
      document.getElementById("emailResult").innerText = data.email_content;
    })
    .catch((error) => {
      alert("There was a problem with the fetch operation: " + error.message);
    })
    .finally(() => {
      document.getElementById("loadingOverlay").style.display = "none"; // Hide overlay and spinner
    });
}

function generateSummary() {
  document.getElementById("loadingOverlay").style.display = "flex"; // Show overlay and spinner

  const startDate = document.getElementById("startDate").value;
  const endDate = document.getElementById("endDate").value;
  fetch("/generateSummary", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `start_date=${startDate}&end_date=${endDate}`,
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((errorData) => {
          throw new Error(errorData.message);
        });
      }
      return response.json();
    })
    .then((data) => {
      document.getElementById("summaryResult").innerText = data.summary_result;
    })
    .catch((error) => {
      alert("There was a problem with the fetch operation: " + error.message);
    })
    .finally(() => {
      document.getElementById("loadingOverlay").style.display = "none"; // Hide overlay and spinner
    });
}

function addTask() {
  const task = document.getElementById("newTask").value;
  const date = document.getElementById("taskDate").value;
  fetch("/addTask", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `task=${task}&date=${date}`,
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((errorData) => {
          throw new Error(errorData.message);
        });
      }
      return response.json();
    })
    .then((data) => {
      alert(data.message);
      location.reload(); // This line will refresh the page
    })
    .catch((error) => {
      alert("Please enter a task and a date");
    });
}

function deleteTask(taskId) {
  fetch(`/deleteTask/${taskId}`, {
    method: "POST",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      alert(data.message);
      location.reload(); // This line will refresh the page
    })
    .catch((error) => {
      alert("There was a problem with the fetch operation: " + error.message);
    });
}
