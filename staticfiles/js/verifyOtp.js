 document.addEventListener("DOMContentLoaded", () => {
    const email = localStorage.getItem("reset_email");
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
        
        try {
           const response = await fetch("/api/verify-reset-otp/", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ email, otp })
        });

        if (response.ok) {
          alert("OTP verified successfully");  
            window.location.href = "/set-password/";
        } else {
            document.getElementById("error-message").style.display = "block";
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