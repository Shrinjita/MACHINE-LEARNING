import cv2
import RPi.GPIO as GPIO
import time

# GPIO pin for the door lock control
lock_pin = 17

# Initialize the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(lock_pin, GPIO.OUT)

# Load the Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the camera (use the correct camera index or video file path)
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Convert the frame to grayscale for face detection
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    # Check if faces are detected
    if len(faces) > 0:
        # Unlock the door
        GPIO.output(lock_pin, GPIO.HIGH)
    else:
        # Lock the door
        GPIO.output(lock_pin, GPIO.LOW)

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame with face rectangles
    cv2.imshow('Face Detection', frame)

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera, close OpenCV windows, and cleanup GPIO
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()
