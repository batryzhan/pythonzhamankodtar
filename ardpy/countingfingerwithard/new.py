import cv2
import controller as cnt
from cvzone.HandTrackingModule import HandDetector
import time

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Camera setup
video = cv2.VideoCapture(0)
video.set(cv2.CAP_PROP_FPS, 60)         # Ask webcam for 60 fps
video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# FPS control
fps = 60
delay = 1.0 / fps
prev_time = 0

while True:
    current_time = time.time()
    if (current_time - prev_time) >= delay:   # Limit to ~60 fps
        prev_time = current_time

        ret, frame = video.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        hands, img = detector.findHands(frame)

        if hands:
            lmList = hands[0]
            fingerUp = detector.fingersUp(lmList)

            cnt.led(fingerUp)

            # Finger count text
            counts = {
                (0,0,0,0,0): "Finger count: 0",
                (0,1,0,0,0): "Finger count: 1",
                (0,1,1,0,0): "Finger count: 2",
                (0,1,1,1,0): "Finger count: 3",
                (0,1,1,1,1): "Finger count: 4",
                (1,1,1,1,1): "Finger count: 5"
            }

            if tuple(fingerUp) in counts:
                cv2.putText(frame, counts[tuple(fingerUp)], (20, 460),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255),
                            1, cv2.LINE_AA)

        cv2.imshow("frame", frame)

    # Quit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
cv2.destroyAllWindows()
