
document.addEventListener("DOMContentLoaded", () => {
    const verifyForm = document.getElementById("verifyForm");
    verifyForm.addEventListener("submit", async (event) => {
        event.preventDefault(); 
        const otpInputs = document.querySelectorAll(".otp");
        let otp = "";
        otpInputs.forEach(input => {
            otp += input.value.trim();
        })
        if (otp.length !== 6) {
            displayError("Please enter a valid 6-digit OTP.");
            return;
        }
        const urlParams = new URLSearchParams(window.location.search);
        const username = urlParams.get("username");
        if (!username) {
            displayError("Username is missing. Please try again.");
            return;
        }
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        try {
            const response = await fetch("/api/verify-otp/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                   "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ username, otp }), // Send username and OTP
            });
            const data = await response.json();
            if (response.ok) {
                alert("Account verified successfully! Redirecting to login...");
                window.location.href = "/login/";
            }else if(response.status === 401){
                displayError( "Invalid OTP. A new OTP has been sent to your email. Please enter the new OTP.");
                otpInputs.forEach(input => input.value="");
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