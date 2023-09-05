
const aboutContent = document.getElementById("about-content");
const projectsContent = document.getElementById("projects-content");

setTimeout(() => {
    aboutContent.style.opacity = "10";
    aboutContent.style.transform = "translateY(0)";
}, 1000); // Fade in and slide in about content after 1 second

setTimeout(() => {
    projectsContent.style.opacity = "10";
    projectsContent.style.transform = "translateY(0)";
}, 2000); // Fade in and slide in projects content after 2 seconds