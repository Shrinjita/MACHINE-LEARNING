// dynamic.js

// Function to toggle the sidebar on small screens
function toggleSidebar() {
    var sidebar = document.getElementById("myNavbar");
    if (sidebar.style.display === "block") {
      sidebar.style.display = "none";
    } else {
      sidebar.style.display = "block";
    }
  }
  
  // Event listener for toggling sidebar
  document.addEventListener("DOMContentLoaded", function () {
    var sidebarToggle = document.getElementById("sidebarToggle");
    if (sidebarToggle) {
      sidebarToggle.addEventListener("click", function () {
        toggleSidebar();
      });
    }
  });
  // server.js

const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

// Body parser middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Endpoint for sending a message
app.post('/send-message', (req, res) => {
  const { name, email, subject, message } = req.body;
  
  // Here you can implement logic to send the message, such as sending an email
  
  res.send('Message sent successfully!');
});

// Endpoint for downloading the resume
app.get('/download-resume', (req, res) => {
  const resumePath = path.join(__dirname, 'resume.pdf');
  
  // Here you can implement logic to read the resume file and send it as a response
  fs.readFile(resumePath, (err, data) => {
    if (err) {
      console.error(err);
      return res.status(500).send('Internal Server Error');
    }
    
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', 'attachment; filename="resume.pdf"');
    res.send(data);
  });
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});

  