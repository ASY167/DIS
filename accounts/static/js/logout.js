document.addEventListener("DOMContentLoaded", () => {
    const logoutBtn = document.getElementById("logoutBtn");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", async () => {
            const refreshToken = localStorage.getItem("refresh");

            if (!refreshToken) {
                alert("No session found.");
                window.location.href = "/login/";
                return;
            }

            try {
                const response = await fetch("/api/logout/", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ refresh: refreshToken })
                });

                localStorage.removeItem("access");
                localStorage.removeItem("refresh");
                localStorage.removeItem("username");

                if (response.ok) {
                    alert("Logged out successfully.");
                } else {
                    alert("Logout failed.");
                }

                window.location.href = "/login/";

            } catch (error) {
                console.error("Logout error:", error);
                alert("An error occurred. Try again.");
            }
        });
    }
});
