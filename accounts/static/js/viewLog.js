document.addEventListener("DOMContentLoaded", () => {
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
        alert("Session expired or not logged in.");
        window.location.href = "/login/";
        return;
    }

    fetch("/api/view-login-activity/", {
        method: "GET",
        headers: {
            "Authorization": `Bearer ${accessToken}`,
            "Content-Type": "application/json"
        }
    })
    .then(res => {
        if (!res.ok) {
            throw new Error("Failed to fetch user profile.");
        }
        return res.json();
    })
    .then(data => {
        const logsContainer = document.querySelector(".logs-info");
        logsContainer.innerHTML = "";
    
        data.forEach(log => {
            logsContainer.innerHTML += `
                <div class="log-entry">
                    <p><strong>id:</strong> ${log.id}</p>
                    <p><strong>action:</strong> ${log.action}</p>
                    <p><strong>user:</strong> ${log.user}</p>
                    <p><strong>ip_address:</strong> ${log.ip_address}</p>
                    <p><strong>was_successful:</strong> ${log.was_successful}</p>
                    <p><strong>timestamp:</strong> ${new Date(log.timestamp).toDateString()}</p>
                    <hr>
                </div>
            `;
        });
    })    
    .catch(err => {
        console.error("logs load error:", err);
        alert("Could not load logs.");
    });
});
