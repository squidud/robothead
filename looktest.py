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

face_cascade = cv2.CascadeClassifier(  # type: ignore[attr-defined]
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'  # type: ignore[attr-defined]
)

cap = cv2.VideoCapture(0)  # type: ignore[attr-defined]

# --- Tuning ---
ALPHA = 0.25         # EMA smoothing per frame (higher = faster/less smooth)
LOST_FRAMES = 10     # Consecutive no-face frames before returning to center
RETURN_ALPHA = 0.06  # Speed of return to center

# --- State ---
smooth_lr = 0.0
smooth_ud = 0.0
commanded_lr = 0     # Last integer degree sent to each servo
commanded_ud = 0
frames_since_face = LOST_FRAMES

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # type: ignore[attr-defined]
    fh, fw = frame.shape[:2]

    # Stricter detection: minNeighbors=8 and minSize=(80,80) filter out non-faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=8,
        minSize=(80, 80)
    )

    if len(faces) > 0:
        frames_since_face = 0

        # Track the largest face — most likely the primary person
        x, y, w, h = max(faces, key=lambda f: f[2] * f[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  # type: ignore[attr-defined]

        cx = x + w // 2
        cy = y + h // 2
        dx = cx - fw // 2
        dy = cy - fh // 2

        # Map pixel offset to angle — scale so frame edges = ±90°
        target_lr = max(min(dx / (fw / 2) * 90, 90), -90)
        target_ud = max(min(-dy / (fh / 2) * 90, 90), -90)

        # EMA: blend current smooth value toward target
        smooth_lr += ALPHA * (target_lr - smooth_lr)
        smooth_ud += ALPHA * (target_ud - smooth_ud)
    else:
        frames_since_face += 1
        # Only pull back to center after several consecutive missed frames
        # This prevents brief detection gaps from jerking the eyes around
        if frames_since_face >= LOST_FRAMES:
            smooth_lr += RETURN_ALPHA * (0.0 - smooth_lr)
            smooth_ud += RETURN_ALPHA * (0.0 - smooth_ud)

    # Round to nearest integer degree — only command servo when the value
    # actually changes, avoiding flooding PWM with sub-degree noise
    new_lr = int(round(smooth_lr))
    new_ud = int(round(smooth_ud))

    if new_lr != commanded_lr:
        commanded_lr = new_lr
        eyeslr.angle = commanded_lr

    if new_ud != commanded_ud:
        commanded_ud = new_ud
        eyesud.angle = commanded_ud

    status = f"faces={len(faces)}  lost={frames_since_face}  lr={commanded_lr}  ud={commanded_ud}"
    cv2.putText(frame, status, (10, 20),  # type: ignore[attr-defined]
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)  # type: ignore[attr-defined]
    cv2.imshow('Face Detection', frame)  # type: ignore[attr-defined]

    if cv2.waitKey(1) & 0xFF == ord('q'):  # type: ignore[attr-defined]
        break

cap.release()
cv2.destroyAllWindows()  # type: ignore[attr-defined]
