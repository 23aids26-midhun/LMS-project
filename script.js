// Simple form validation and dynamic feedback

document.addEventListener("DOMContentLoaded", () => {
    // Handle student form
    const studentForm = document.querySelector("form[action='/student']");
    if (studentForm) {
        studentForm.addEventListener("submit", (e) => {
            const name = studentForm.querySelector("input[name='name']").value.trim();
            const email = studentForm.querySelector("input[name='email']").value.trim();

            if (!name || !email) {
                e.preventDefault();
                alert("Please fill out all student fields!");
            }
        });
    }

    // Handle trainer form
    const trainerForm = document.querySelector("form[action='/trainer']");
    if (trainerForm) {
        trainerForm.addEventListener("submit", (e) => {
            const name = trainerForm.querySelector("input[name='name']").value.trim();
            const subject = trainerForm.querySelector("input[name='subject']").value.trim();

            if (!name || !subject) {
                e.preventDefault();
                alert("Please fill out all trainer fields!");
            }
        });
    }

    // Handle institute form
    const instituteForm = document.querySelector("form[action='/institute']");
    if (instituteForm) {
        instituteForm.addEventListener("submit", (e) => {
            const name = instituteForm.querySelector("input[name='name']").value.trim();
            const location = instituteForm.querySelector("input[name='location']").value.trim();

            if (!name || !location) {
                e.preventDefault();
                alert("Please fill out all institute fields!");
            }
        });
    }

    // Example: highlight nav links when clicked
    const navLinks = document.querySelectorAll("nav a");
    navLinks.forEach(link => {
        link.addEventListener("click", () => {
            navLinks.forEach(l => l.classList.remove("active"));
            link.classList.add("active");
        });
    });
});
