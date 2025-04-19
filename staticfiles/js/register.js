document.addEventListener("DOMContentLoaded", () => {
    const registerForm = document.getElementById("registerForm");

    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent default form submission

        // Get form values
        const username = document.getElementById("username").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        try {
            // Send registration data to the server
            const response = await fetch("/api/register/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ username, email, password }),
            });

            const data = await response.json();

            if (response.ok) {
                alert("Registration successful! Check your email for the OTP.");
                // Redirect to the OTP verification page
                window.location.href = `/verify-otp/?username=${encodeURIComponent(username)}`;
            } else {
                alert(`Error: ${JSON.stringify(data)}`);
            }
        } catch (error) {
            console.error("Error:", error);
            alert("An error occurred. Please try again.");
        }
    });
});

