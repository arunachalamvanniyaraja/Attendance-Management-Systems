Attendance Management System


The Attendance Management System is a web-based application designed to manage attendance using face recognition technology. It allows users to add faces, mark attendance, and view attendance records in a user-friendly interface.

Features
Add Face: Upload a face image and associate it with a name.

Mark Attendance: Capture an image using the webcam and mark attendance for recognized faces.

View Attendance: View attendance records in a tabular format.

User Authentication: Secure login and signup functionality.

Responsive Design: Works seamlessly on both desktop and mobile devices.

Technologies Used:
1. Frontend:

HTML, CSS, JavaScript

2. Flask (for templating)

3. Backend:

Python (Flask framework)

4. Face Recognition:

face_recognition library

5. Database:

CSV files for storing face encodings, attendance records, and user credentials.

6. Webcam Integration:

OpenCV (cv2)

Prerequisites
Before running the project, ensure you have the following installed:

Python 3.8+

Pip (Python package manager)

Git (optional, for cloning the repository)

Installation
Follow these steps to set up the project on your local machine:

1. Clone the Repository
git clone https://github.com/arunachalamvanniyaraja/Attendance-Management-Systems.git
cd attendance-management-system
2. Set Up a Virtual Environment (Optional but Recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
3. Install Dependencies
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the root directory and add the following:

plaintext
Copy
SECRET_KEY=your_secret_key_here
5. Run the Application
bash
Copy
python app.py
The application will be available at http://127.0.0.1:5000.

Usage
1. Sign Up
Navigate to the Sign Up page.

Enter a username and password to create an account.

2. Log In
Use your credentials to log in to the system.

3. Add Face
Go to the Add Face section.

Enter a name and upload an image of the person.

Click Add Face to save the face encoding.

4. Mark Attendance
Go to the Mark Attendance section.

Click Mark Attendance to capture an image using the webcam.

The system will recognize the face and mark attendance.

5. View Attendance
Go to the View Attendance section.

Click View Attendance to see the attendance records.

6. Log Out
Click the Logout button to log out of the system.

File Structure

attendance-management-system/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables
├── README.md               # Project documentation
├── static/
│   ├── css/
│   │   └── styles.css      # CSS styles
│   ├── js/
│   │   ├── script.js       # Main JavaScript file
│   │   ├── login.js        # Login functionality
│   │   └── signup.js       # Signup functionality
│   └── images/             # Folder for storing face images
├── templates/
│   ├── index.html          # Main page
│   ├── login.html          # Login page
│   └── signup.html         # Signup page
├── face_encodings.pkl      # Face encodings (generated at runtime)
├── attendance.csv          # Attendance records (generated at runtime)
└── credentials.csv         # User credentials (generated at runtime)