document.addEventListener("DOMContentLoaded", () => {
    const accessToken = localStorage.getItem("access");
    const username = localStorage.getItem("username");

    if (!accessToken || !username) {
        alert("You're not logged in. Redirecting to login page...");
        window.location.href = "/login/";
        return;
    }

    // Display username in dashboard
    const usernameDisplay = document.getElementById("usernameDisplay");
    if (usernameDisplay) {
        usernameDisplay.textContent = username;
    }

    // Optionally verify token by pinging a protected route
    fetch("/api/view-login-activity/", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${accessToken}`
        }
    })
    .then(res => {
        if (res.status === 401) {
            throw new Error("Token expired or invalid");
        }
        return res.json();
    })
    .then(data => {
        console.log("Login activity verified, token is valid");
    })
    .catch(err => {
        console.error("Error:", err);
        alert("Session expired. Please login again.");
        localStorage.clear();
        window.location.href = "/login/";
    });
});
