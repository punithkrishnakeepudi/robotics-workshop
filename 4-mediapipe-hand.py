import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

# Hands() loads the model that ships inside mediapipe, no file to download
with mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.5) as hands:
    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)  # mirror, so your right hand shows on the right

        # mediapipe wants RGB, opencv gives BGR
        result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        if result.multi_hand_landmarks:  # None when no hand is on screen
            for hand_landmarks in result.multi_hand_landmarks:  # 21 points per hand
                # draws the joints and the bones between them for you
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow("Hand Landmarks", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
