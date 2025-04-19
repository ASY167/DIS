document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent default form submission

        // Get form values
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        try {
            // Send POST request to the login API
            const response = await fetch("/api/login/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "CSRFToen": csrfToken,
                },
                body: JSON.stringify({ username, password }),
            });

            const data = await response.json();

            if (response.ok) {
                alert(data.message); // Show success message
            } else {
                alert(`Error: ${JSON.stringify(data)}`); // Show error message
            }
        } catch (error) {
            alert("An error occurred during login. Please try again.");
            console.error(error);
        }
    });
});
