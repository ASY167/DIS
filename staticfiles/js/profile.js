document.addEventListener("DOMContentLoaded", () => {
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
        alert("Session expired or not logged in.");
        window.location.href = "/login/";
        return;
    }

    fetch("/api/get-profile/", {
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
        document.querySelector(".profile-info").innerHTML = `
            <p><strong>Username:</strong> ${data.username}</p>
            <p><strong>First Name:</strong> ${data.first_name || "Not set"}</p>
            <p><strong>Last Name:</strong> ${data.last_name || "Not set"}</p>
            <p><strong>Email:</strong> ${data.email}</p>
            <p><strong>Bio:</strong> ${data.bio || "No bio provided"}</p>
            <p><strong>Joined:</strong> ${new Date(data.date_joined).toDateString()}</p>
        `;
    })
    .catch(err => {
        console.error("Profile load error:", err);
        alert("Could not load profile.");
    });
});
