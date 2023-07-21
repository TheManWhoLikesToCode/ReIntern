// Function to add a new task to the task list
function addTask() {
    const taskInput = document.getElementById('newTask');
    const taskList = document.getElementById('taskList');
    const taskText = taskInput.value.trim();

    if (taskText !== '') {
        const li = document.createElement('li');
        li.textContent = taskText;
        taskList.appendChild(li);
        taskInput.value = '';
    }
}

// Function to generate an email content using the tasks entered
function generateEmail() {
    const taskList = document.getElementById('taskList');
    const tasks = Array.from(taskList.getElementsByTagName('li')).map(li => li.textContent);
    const emailContent = document.getElementById('emailContent');
    emailContent.textContent = `Hello Manager!,\n\nI wanted to share my progress and accomplishments with you for the week. Here are some of the tasks I have been working on:\n\n${tasks.join('\n')}\n\nBest regards,\n[Your Name]`;
    // this line above is just a placeholder for now, we will figure out how to include the openai api for chatgpt so that these can be generated when requested by the user 
}
