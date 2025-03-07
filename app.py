from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import cv2
import numpy as np
import datetime
import pandas as pd
import face_recognition
import os

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key_here'

# Paths
PROJECT_FOLDER = r"D:\FinalPhase"
FACES_DIR = os.path.join(PROJECT_FOLDER, "static", "images", "faces")
ENCODINGS_FILE = os.path.join(PROJECT_FOLDER, "face_encodings.pkl")
ATTENDANCE_CSV = os.path.join(PROJECT_FOLDER, "attendance.csv")
CREDENTIALS_CSV = os.path.join(PROJECT_FOLDER, "credentials.csv")

# Ensure directories exist
os.makedirs(FACES_DIR, exist_ok=True)

# Load or create face encodings
face_encodings = {}
if os.path.exists(ENCODINGS_FILE):
    face_encodings = pd.read_pickle(ENCODINGS_FILE)

# Ensure attendance.csv exists
if not os.path.exists(ATTENDANCE_CSV):
    with open(ATTENDANCE_CSV, "w") as f:
        f.write("Name,Timestamp\n")

# Ensure credentials.csv exists
if not os.path.exists(CREDENTIALS_CSV):
    with open(CREDENTIALS_CSV, "w") as f:
        f.write("Username,Password\n")

@app.route("/")
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")

        credentials_df = pd.read_csv(CREDENTIALS_CSV)
        user = credentials_df[(credentials_df["Username"] == username) & (credentials_df["Password"] == password)]

        if not user.empty:
            session['username'] = username
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Invalid username or password"})
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")

        credentials_df = pd.read_csv(CREDENTIALS_CSV)
        if username in credentials_df["Username"].values:
            return jsonify({"status": "error", "message": "Username already exists"})

        new_user = pd.DataFrame([[username, password]], columns=["Username", "Password"])
        credentials_df = pd.concat([credentials_df, new_user], ignore_index=True)
        credentials_df.to_csv(CREDENTIALS_CSV, index=False)

        return jsonify({"status": "success"})
    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Existing routes for add_face, mark_attendance, and view_attendance remain unchanged


@app.route("/add_face", methods=["POST"])
def add_face():
    name = request.form["name"]
    image = request.files["image"]
    
    # Save image
    image_path = os.path.join(FACES_DIR, f"{name}.jpg")
    image.save(image_path)
    
    # Create face encoding
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)
    
    if len(encodings) == 0:
        return jsonify({"status": "error", "message": "No face detected in image"})
    
    face_encodings[name] = encodings[0]
    pd.to_pickle(face_encodings, ENCODINGS_FILE)
    
    return jsonify({"status": "success", "message": f"Face added for {name}"})

@app.route("/mark_attendance", methods=["POST"])
def mark_attendance():
    try:
        # Capture image from webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return jsonify({"status": "error", "message": "Failed to open webcam"}), 400

        ret, frame = cap.read()
        cap.release()
        
        if not ret:
            return jsonify({"status": "error", "message": "Failed to capture image from webcam"}), 400

        # Convert image to RGB format
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)
        if not face_locations:
            return jsonify({"status": "error", "message": "No faces detected in the captured image"}), 400

        # Get face encodings
        face_encodings_list = face_recognition.face_encodings(rgb_frame, face_locations)
        if not face_encodings_list:
            return jsonify({"status": "error", "message": "Could not extract face features"}), 400

        # Recognize faces
        recognized_names = []
        for face_encoding in face_encodings_list:
            matches = face_recognition.compare_faces(
                list(face_encodings.values()), 
                face_encoding,
                tolerance=0.6
            )
            
            # Find best match
            face_distances = face_recognition.face_distance(
                list(face_encodings.values()), 
                face_encoding
            )
            if len(face_distances) == 0:
                return jsonify({"status": "error", "message": "No face encodings available for comparison"}), 400

            best_match_index = np.argmin(face_distances)
            
            if matches[best_match_index]:
                name = list(face_encodings.keys())[best_match_index]
            else:
                name = "Unknown"
            recognized_names.append(name)

        # Save attendance
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attendance_df = pd.read_csv(ATTENDANCE_CSV) if os.path.exists(ATTENDANCE_CSV) else pd.DataFrame(columns=["Name", "Timestamp"])
        for name in recognized_names:
            new_entry = pd.DataFrame([[name, timestamp]], columns=["Name", "Timestamp"])
            attendance_df = pd.concat([attendance_df, new_entry], ignore_index=True)
        
        attendance_df.to_csv(ATTENDANCE_CSV, index=False)

        # Set the current user in the session
        session["current_user"] = recognized_names[0]  # Assuming the first recognized name is the current user
        print("Current User (Mark Attendance):", session.get("current_user"))

        return jsonify({
            "status": "success",
            "message": f"Attendance marked for: {', '.join(recognized_names)}",
            "names": recognized_names
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }), 500

@app.route("/view_attendance")
def view_attendance():
    try:
        # Debugging: Print the current user and attendance data
        print("Current User (View Attendance):", session.get("current_user"))

        # Load attendance data
        attendance_df = pd.read_csv(ATTENDANCE_CSV) if os.path.exists(ATTENDANCE_CSV) else pd.DataFrame(columns=["Name", "Timestamp"])

        # Debugging: Print the attendance DataFrame
        print("Attendance DataFrame:", attendance_df)

        # Convert Timestamp to datetime for sorting
        attendance_df["Timestamp"] = pd.to_datetime(attendance_df["Timestamp"])

        # Get the current user's name from the session
        current_user = session.get("current_user")

        # Check if the current user has marked attendance
        if not current_user or current_user not in attendance_df["Name"].values:
            return jsonify({
                "status": "error",
                "message": "Mark your attendance first."
            })

        # Get the last marked attendance entry (most recent)
        last_attendance = attendance_df.sort_values(by="Timestamp", ascending=False).iloc[0:1]  # Get only the first row

        # Return the last attendance as an HTML table
        return jsonify({
            "status": "success",
            "html": last_attendance.to_html(
                classes='table',
                index=False,
                border=0
            )
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": f"Error loading attendance: {str(e)}"
        })


if __name__ == "__main__":
    app.run(debug=True)