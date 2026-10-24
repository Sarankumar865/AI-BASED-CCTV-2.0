from ultralytics import YOLO
import cv2

# Load the YOLO AI model
print("Loading YOLO model...")
model = YOLO("yolo26n.pt")

# Open the laptop webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    print("Check camera permissions or try camera index 1.")
    exit()

print("Webcam started!")
print("Press Q to close the camera.")

while True:
    # Capture one video frame
    ret, frame = cap.read()

    if not ret:
        print("Error: Cannot read webcam frame.")
        break

    # Detect objects in the frame
    results = model(frame, verbose=False)

    # Draw boxes and labels
    detected_frame = results[0].plot()

    # Display live video
    cv2.imshow("AI CCTV 2.0 - Live Detection", detected_frame)

    # Press Q to quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release webcam and close windows
cap.release()
cv2.destroyAllWindows()

print("AI CCTV stopped.")