from ultralytics import YOLO
import cv2

print("Loading AI model...")

# Load a small pretrained object-detection model
model = YOLO("yolo26n.pt")

print("Detecting objects in sample image...")

# Download and analyse a sample image
image_url = "https://ultralytics.com/images/bus.jpg"
results = model(image_url)

# Save the image with detection boxes
for result in results:
    output_image = result.plot()
    cv2.imwrite("detected_result.jpg", output_image)

    print("\nDetected objects:")
    for box in result.boxes:
        class_id = int(box.cls[0])
        name = model.names[class_id]
        confidence = float(box.conf[0])

        print(f"{name}: {confidence:.2f}")

print("\nDone! Check detected_result.jpg")