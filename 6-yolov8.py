import cv2
from ultralytics import YOLO

# Load the YOLOv8 nano model
# It will automatically download 'yolov8n.pt' if it's not present
model = YOLO('yolov8n.pt') 

# Open the default webcam (index 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

print("Starting YOLOv8 Object Detection. Press 'q' to quit.")

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break
        
    # Run YOLOv8 inference on the frame
    # verbose=False stops it printing a report line for every single frame
    results = model(frame, verbose=False)

    # .plot() returns the image array with bounding boxes and labels drawn
    annotated_frame = results[0].plot()

    # Display the annotated frame
    cv2.imshow("YOLOv8 Object Detection", annotated_frame)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
