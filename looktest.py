from gpiozero import AngularServo
from time import sleep
import random
import cv2

# Create servos on different GPIO pins
eyeslr = AngularServo(12)  # eyes l/r
eyesud = AngularServo(13)  # eyes up/down
jaw = AngularServo(18)  # jaw
necklr = AngularServo(19)   # neck l/r

# Control them using angles
eyeslr.angle = 0
eyesud.angle = 0
jaw.angle = 0
necklr.angle = 0

#Let's load the pre-trained Haar Cascade Classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

#here we will initialize video capture (0 for built-in webcam)
cap = cv2.VideoCapture(0)

while True:
    #this will read frame-by-frame from the webcam
    ret, frame = cap.read()

    face_pos = None  # Initialize face position variable
    
    #Convert frame to grayscale (Haar Cascade works better with grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    #this will draw rectangles around detected faces as shown
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        face_pos = (x + w//2, y + h//2)  # Get the center of the detected face

        # move servos based on face position (simple proportional control)
        if face_pos:
            frame_center = (frame.shape[1]//2, frame.shape[0]//2)
            dx = face_pos[0] - frame_center[0]
            dy = face_pos[1] - frame_center[1]

            # Adjust angles based on position (these values may need tuning)
            eyeslr.angle = max(min(dx / 10, 90), -90)  # Scale and limit to [-90, 90]
            eyesud.angle = max(min(-dy / 10, 90), -90)  # Invert y-axis and limit to [-90, 90]
        
    
    #display the resulting frame with detected faces
    cv2.imshow('Face Detection', frame)
    
    #break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#release the video capture and close windows
cap.release()
cv2.destroyAllWindows()

