from ultralytics import YOLO
import cv2
import sqlite3
from datetime import datetime
import time

# 1. Create and connect database
connection = sqlite3.connect("cctv_events.db")
cursor = connection.cursor()

# Create events table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_time TEXT NOT NULL,
        event_type TEXT NOT NULL,
        description TEXT NOT NULL
    )
""")

# Create camera status table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS camera_status (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        updated_at TEXT NOT NULL,
        people_count INTEGER NOT NULL,
        zone_occupied INTEGER NOT NULL
    )
""")

connection.commit()


# 2. Save security events
def save_event(event_type, description):
    event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        """INSERT INTO events
           (event_time, event_type, description)
           VALUES (?, ?, ?)""",
        (event_time, event_type, description)
    )

    connection.commit()
    print(f"[SAVED] {event_time} | {event_type} | {description}")


# 3. Load YOLO model
print("Loading YOLO model...")
model = YOLO("yolo26n.pt")

# 4. Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam.")
    connection.close()
    raise SystemExit

# 5. Alert settings
alert_cooldown = 5
last_alert_time = 0
last_status_save = 0
zone_was_occupied = False

print("AI CCTV 2.0 started!")
print("Press Q to stop the camera.")

try:
    while True:

        # 6. Capture webcam frame
        ret, frame = cap.read()

        if not ret:
            print("Cannot read camera frame.")
            break

        # 7. Detect objects
        results = model(frame, verbose=False)
        result = results[0]
        display = result.plot()

        height, width = frame.shape[:2]

        # 8. Define restricted zone
        x1 = int(width * 0.55)
        y1 = int(height * 0.25)
        x2 = int(width * 0.95)
        y2 = int(height * 0.90)

        cv2.rectangle(
            display,
            (x1, y1),
            (x2, y2),
            (0, 0, 255),
            2
        )

        cv2.putText(
            display,
            "RESTRICTED ZONE",
            (x1, max(25, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )

        # 9. Count people and check zone
        people_count = 0
        person_in_zone = False

        for box in result.boxes:
            class_id = int(box.cls[0])
            name = model.names[class_id]

            if name == "person":
                people_count += 1

                bx1, by1, bx2, by2 = box.xyxy[0].tolist()

                center_x = int((bx1 + bx2) / 2)
                center_y = int((by1 + by2) / 2)

                if (
                    x1 <= center_x <= x2
                    and y1 <= center_y <= y2
                ):
                    person_in_zone = True

        # 10. Display people count
        cv2.putText(
            display,
            f"People Count: {people_count}",
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        # 11. Save latest camera status once per second
        current_time = time.time()

        if current_time - last_status_save >= 1:
            cursor.execute("""
                INSERT INTO camera_status
                    (id, updated_at, people_count, zone_occupied)
                VALUES (1, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    updated_at = excluded.updated_at,
                    people_count = excluded.people_count,
                    zone_occupied = excluded.zone_occupied
            """, (
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                people_count,
                int(person_in_zone)
            ))

            connection.commit()
            last_status_save = current_time

        # 12. Restricted-zone alert
        if person_in_zone:
            cv2.putText(
                display,
                "WARNING: PERSON IN ZONE!",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 0, 255),
                2
            )

            # Save on entry, then at most every 5 seconds
            if (
                not zone_was_occupied
                or current_time - last_alert_time >= alert_cooldown
            ):
                save_event(
                    "RESTRICTED_ZONE",
                    f"Person detected in restricted zone; "
                    f"people visible: {people_count}"
                )

                last_alert_time = current_time

        zone_was_occupied = person_in_zone

        # 13. Display live security monitor
        cv2.imshow(
            "AI CCTV 2.0 - Database Monitor",
            display
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    # 14. Release camera and close database
    cap.release()
    cv2.destroyAllWindows()
    connection.close()
    print("Camera stopped. Database connection closed.")