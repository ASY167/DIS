document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("changePasswordForm");
    const accessToken = localStorage.getItem("access");

    if (!accessToken) {
        alert("Session expired. Please log in again.");
        window.location.href = "/login/";
        return;
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const oldPassword = document.getElementById("oldPassword").value;
        const newPassword = document.getElementById("newPassword").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (newPassword !== confirmPassword) {
            alert("New passwords do not match.");
            return;
        }

        try {
            const response = await fetch("/api/change-password/", {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    old_password: oldPassword,
                    new_password: newPassword
                })
            });

            const data = await response.json();

            if (response.ok) {
                alert("Password changed successfully.");
                window.location.href = "/login/";
            } else {
                alert(data.error || "Password change failed.");
            }

        } catch (err) {
            console.error("Password change error:", err);
            alert("An error occurred. Please try again.");
        }
    });
});
