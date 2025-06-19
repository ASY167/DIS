document.addEventListener("DOMContentLoaded", () => {
        console.log("Edit Profile JS loaded");

    const editProfileForm = document.getElementById("editProfileForm");
    const accessToken = localStorage.getItem("access");

    editProfileForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = {
            username: document.getElementById("username").value,
            first_name: document.getElementById("firstName").value,
            last_name: document.getElementById("lastName").value,
            email: document.getElementById("email").value,
            bio: document.getElementById("bio").value
        };

        try {
            const response = await fetch("/api/update-profile/", {
                method: "PUT",
                headers: {
                    "Authorization": `Bearer ${accessToken}`,
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                alert("Profile updated successfully!");
                window.location.href = "/profile/";
            } else {
                console.error("Update failed api:", data);
                alert(data.detail || data.error || "Update failed. Please try again.");
            }
        } catch (error) {
            console.error("Error updating profile:", error);
            alert("An unexpected error occurred.");
        }
    });
});
