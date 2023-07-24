function generateEmail() {
  const summary = document.getElementById("emailContent").innerText;
  fetch("/generate_email", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ summary: summary }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.getElementById("emailResult").innerText = data.email_content;
    });
}

function generateSummary() {
  const startDate = document.getElementById("startDate").value;
  const endDate = document.getElementById("endDate").value;
  fetch("/generateSummary", {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body: `start_date=${startDate}&end_date=${endDate}`,
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.getElementById("summaryResult").innerText = data.summary_result;
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
    .then((response) => response.json())
    .then((data) => console.log(data));
}

function deleteTask(taskId) {
  fetch(`/deleteTask/${taskId}`, {
    method: "POST",
  })
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      // You can add code here to update the UI based on the server's response.
    });
}
