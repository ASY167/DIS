
document.addEventListener("DOMContentLoaded", () => {
    const verifyForm = document.getElementById("verifyForm");

    verifyForm.addEventListener("submit", async (event) => {
        event.preventDefault(); // Prevent form reload

        // Combine OTP values into a single string
        const otpInputs = document.querySelectorAll(".otp");
        let otp = "";
        otpInputs.forEach(input => {
            otp += input.value.trim();
        });

        // Validate OTP length
        if (otp.length !== 6) {
            displayError("Please enter a valid 6-digit OTP.");
            return;
        }

        // Extract username from query parameters
        const urlParams = new URLSearchParams(window.location.search);
        const username = urlParams.get("username");

        if (!username) {
            displayError("Username is missing. Please try again.");
            return;
        }

        // Send OTP to server
        try {
            const response = await fetch("/api/verify-otp/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken(), // Include CSRF token
                },
                body: JSON.stringify({ username, otp }), // Send username and OTP
            });

            const data = await response.json();

            if (response.ok) {
                alert("Account verified successfully! Redirecting to login...");
                window.location.href = "/login/"; // Redirect to login page
            } else {
                displayError(data.error || "Invalid OTP. Please try again.");
            }
        } catch (error) {
            displayError("An error occurred. Please try again later.");
            console.error("Error:", error);
        }
    });

    // Move to the next input box automatically
    window.moveToNext = (current, nextId) => {
        if (current.value.length === current.maxLength) {
            const nextInput = document.getElementById(nextId);
            if (nextInput) nextInput.focus();
        }
    };

    // Display error message
    function displayError(message) {
        const errorDiv = document.getElementById("error-message");
        errorDiv.textContent = message;
        errorDiv.style.display = "block";
    }

});



