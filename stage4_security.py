from ultralytics import YOLO
import cv2
import time

# Load AI model
print("Loading YOLO model...")
model = YOLO("yolo26n.pt")

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam.")
    exit()

# Alert cooldown
last_alert_time = 0
alert_cooldown = 5

print("AI CCTV 2.0 started!")
print("Press Q to stop.")

while True:
    ret, frame = cap.read()

    if not ret:
        print("Cannot read camera frame.")
        break

    # Detect objects
    results = model(frame, verbose=False)
    result = results[0]

    # Draw AI detection boxes
    display = result.plot()

    # Get camera frame size
    height, width = frame.shape[:2]

    # Define restricted zone on the right side
    x1 = int(width * 0.55)
    y1 = int(height * 0.25)
    x2 = int(width * 0.95)
    y2 = int(height * 0.90)

    # Draw restricted zone
    cv2.rectangle(
        display, (x1, y1), (x2, y2),
        (0, 0, 255), 2
    )

    cv2.putText(
        display, "RESTRICTED ZONE",
        (x1, max(25, y1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7, (0, 0, 255), 2
    )

    # Count people visible in this frame
    people_count = 0
    person_in_zone = False

    for box in result.boxes:
        class_id = int(box.cls[0])
        object_name = model.names[class_id]

        if object_name == "person":
            people_count += 1

            # Find the centre of the person detection box
            bx1, by1, bx2, by2 = box.xyxy[0].tolist()
            center_x = int((bx1 + bx2) / 2)
            center_y = int((by1 + by2) / 2)

            # Check whether the centre is inside the zone
            if (x1 <= center_x <= x2 and
                    y1 <= center_y <= y2):
                person_in_zone = True

    # Display people count
    cv2.putText(
        display, f"People Count: {people_count}",
        (20, 35), cv2.FONT_HERSHEY_SIMPLEX,
        0.8, (0, 255, 0), 2
    )

    # Restricted-zone alert with cooldown
    current_time = time.time()

    if person_in_zone:
        cv2.putText(
            display, "WARNING: PERSON IN ZONE!",
            (20, 75), cv2.FONT_HERSHEY_SIMPLEX,
            0.7, (0, 0, 255), 2
        )

        if current_time - last_alert_time >= alert_cooldown:
            print("ALERT: Person detected in restricted zone!")
            last_alert_time = current_time

    # Display live security camera
    cv2.imshow("AI CCTV 2.0 - Security Monitor", display)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()

print("AI CCTV stopped.")