import cv2
import mediapipe as mp

mp_pose = mp.solutions.pose
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Pose() loads the model that ships inside mediapipe, no file to download
with mp_pose.Pose(min_detection_confidence=0.5) as pose:
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # mediapipe wants RGB, opencv gives BGR
        result = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if result.pose_landmarks:  # None when no body is on screen
            # draws the 33 body joints and the bones between them for you
            mp_draw.draw_landmarks(frame, result.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.imshow("Pose Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
