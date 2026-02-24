from gpiozero import AngularServo
import cv2

# Create servos on different GPIO pins
eyeslr = AngularServo(12)  # eyes l/r
eyesud = AngularServo(13)  # eyes up/down
jaw = AngularServo(18)     # jaw
necklr = AngularServo(19)  # neck l/r

# Initialize servos to center
eyeslr.angle = 0
eyesud.angle = 0
jaw.angle = 0
necklr.angle = 0

# Load Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

cap = cv2.VideoCapture(0)

# --- Tunable parameters ---
ALPHA = 0.12          # EMA smoothing (0=frozen, 1=instant snap)
DEAD_ZONE = 2.0       # Degrees — ignore servo updates smaller than this
CONFIRM_FRAMES = 4    # Face must appear this many consecutive frames before tracking
RETURN_SPEED = 0.08   # How fast eyes return to center when no face

# --- State ---
smooth_lr = 0.0
smooth_ud = 0.0
current_lr = 0.0
current_ud = 0.0
face_confirm = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fh, fw = frame.shape[:2]

    # Stricter detection: higher minNeighbors and larger minSize filter out non-faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=8,
        minSize=(80, 80)
    )

    if len(faces) > 0:
        face_confirm = min(face_confirm + 1, CONFIRM_FRAMES)

        # Use the largest detected face — most likely the primary person
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cx = x + w // 2
        cy = y + h // 2
        dx = cx - fw // 2
        dy = cy - fh // 2

        # Map pixel offset to angle range [-90, 90]
        target_lr = max(min(dx / (fw / 2) * 90, 90), -90)
        target_ud = max(min(-dy / (fh / 2) * 90, 90), -90)

        # Only update smoothed target when face is confirmed
        if face_confirm >= CONFIRM_FRAMES:
            smooth_lr += ALPHA * (target_lr - smooth_lr)
            smooth_ud += ALPHA * (target_ud - smooth_ud)
    else:
        face_confirm = max(face_confirm - 1, 0)
        # Smoothly return to center when no confirmed face
        smooth_lr += RETURN_SPEED * (0.0 - smooth_lr)
        smooth_ud += RETURN_SPEED * (0.0 - smooth_ud)

    # Only command the servo if the change exceeds the dead zone
    if abs(smooth_lr - current_lr) > DEAD_ZONE:
        current_lr = smooth_lr
        eyeslr.angle = round(current_lr, 1)

    if abs(smooth_ud - current_ud) > DEAD_ZONE:
        current_ud = smooth_ud
        eyesud.angle = round(current_ud, 1)

    # Show debug info on frame
    status = f"confirmed={face_confirm}/{CONFIRM_FRAMES}  lr={current_lr:.1f}  ud={current_ud:.1f}"
    cv2.putText(frame, status, (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imshow('Face Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
