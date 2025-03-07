// Handle Add Face Form
document.getElementById('add-face-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData();
    formData.append('name', document.getElementById('name').value);
    formData.append('image', document.getElementById('image').files[0]);

    try {
        const response = await fetch('/add_face', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }
        const result = await response.json();
        alert(result.message);
    } catch (error) {
        alert('Error adding face: ' + error.message);
    }
});

// Handle Mark Attendance
document.getElementById('mark-attendance').addEventListener('click', async () => {
    try {
        const response = await fetch('/mark_attendance', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
        }

        const result = await response.json();
        if (result.status === 'success') {
            alert(result.message);
            document.getElementById('view-attendance').click();
        } else {
            alert(`Error: ${result.message}`);
        }
    } catch (error) {
        alert(`Attendance marking failed: ${error.message}`);
    }
});
// Handle View Attendance
document.getElementById('view-attendance').addEventListener('click', async () => {
    try {
        const response = await fetch('/view_attendance');
        const result = await response.json();

        if (result.status === 'error') {
            // Show popup message if the user hasn't marked attendance
            alert(result.message);  // 🚀 Show alert message "Mark your attendance first."
        } else {
            // Display the attendance table
            document.getElementById('attendance-table').innerHTML = result.html;
        }
    } catch (error) {
        alert('Error loading attendance: ' + error.message);
    }
});


// Handle Logout
document.getElementById('logout-button').addEventListener('click', async () => {
    try {
        const response = await fetch('/logout');
        if (response.redirected) {
            window.location.href = response.url;
        }
    } catch (error) {
        alert('Logout failed: ' + error.message);
    }
});

// Show logout button if user is logged in
if (document.getElementById('logout-button')) {
    document.getElementById('logout-button').style.display = 'block';
}