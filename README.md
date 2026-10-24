AI CCTV 2.0 — AI-Based Smart CCTV Surveillance System

Project Overview

AI CCTV 2.0 is a smart surveillance project developed using Python, OpenCV, YOLO, SQLite, and Streamlit. It detects people through a camera, monitors a restricted zone, records events, and displays surveillance information through a dashboard.

Features

- Person Detection: Detects people using a YOLO object-detection model.
- People Counting: Displays the number of detected people.
- Restricted-Zone Monitoring: Detects when a person enters the configured restricted area.
- Event Logging: Stores surveillance events and descriptions in an SQLite database.
- Camera Status Tracking: Saves the latest people count and restricted-zone status.
- Analytics Dashboard: Displays camera status and event history using Streamlit.
- Event Filtering: Filters event records by date and event type.
- CSV Export: Allows event data to be downloaded as a CSV file.
- Daily Event Trend: Displays daily event analytics.

Technologies Used

- Python
- OpenCV
- YOLO (Ultralytics)
- SQLite
- Pandas
- Streamlit

System Requirements

- Windows, Linux, or another compatible operating system
- Python installed
- A webcam or compatible camera
- Internet access for installing dependencies and obtaining the required YOLO model

Installation

1. Clone this repository:
   
   git clone YOUR_REPOSITORY_URL

2. Open the downloaded project folder:
   
   cd AI-CCTV-2.0

3. Create and activate a virtual environment (recommended):
   
   python -m venv .venv
.venv\Scripts\activate

4. Install the dependencies:
   
   pip install -r requirements.txt

5. Ensure the YOLO model file used by your camera script is available. Follow the model's official instructions if it needs to be downloaded separately.

Running the Project

Run the camera detection program using its actual filename. For example:

python main.py

Start the Streamlit dashboard using its actual filename. For example:

streamlit run dashboard.py

Replace "main.py" and "dashboard.py" with the filenames in your repository.

Database

SQLite stores camera status and surveillance events. The database is created or updated locally when the application runs, according to the implementation.

Do not commit personal surveillance records or a live database containing private information.

Testing

The implemented features have been tested in the development environment, including camera detection, people counting, restricted-zone alerts, SQLite event storage, and the Streamlit dashboard.

Future Enhancements

Possible future improvements include user authentication, additional alert methods, and support for multiple cameras. These are future ideas, not currently claimed as implemented features.

Author

SaranKumar G

R P Sarathy Institute of Technology, Salem
Department of Artificial Intelligence and Data Science

Disclaimer

This project is intended for educational and demonstration purposes. Use cameras responsibly and respect privacy and applicable laws.
