import math
import time

import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt

# MQTT Configuration
# Must match the broker and topic in mediapipe/esp8266_mqtt_arm.txt
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "grrr_workshop/esp8266/arm"

# Joint limits copied from the ESP8266 sketch. Keep both files in sync.
# The firmware clamps anything out of range too, this is just the second net.
LIMITS = {
    "base":     (0, 180),
    "shoulder": (20, 160),
    "elbow":    (10, 170),
    "gripper":  (20, 150),
}
JOINTS = ["base", "shoulder", "elbow", "gripper"]

SEND_INTERVAL = 0.05   # seconds -> at most 20 messages per second
DEAD_BAND = 2          # degrees -> ignore hand jitter smaller than this
SMOOTHING = 0.3        # 0 = frozen, 1 = raw and twitchy

# Setup MQTT Client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# MediaPipe Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

# The arm starts at the home position and stays there until a hand shows up
angles = {"base": 90.0, "shoulder": 90.0, "elbow": 90.0, "gripper": 90.0}
last_sent = dict(angles)
last_send_time = 0.0


def remap(value, in_min, in_max, out_min, out_max):
    t = (value - in_min) / (in_max - in_min)
    t = max(0.0, min(1.0, t))  # clamp BEFORE scaling, a servo must never get 200 deg
    return out_min + t * (out_max - out_min)


def distance(a, b):
    return math.hypot(a.x - b.x, a.y - b.y)


def angles_from_hand(hand_landmarks):
    lm = hand_landmarks.landmark
    wrist, middle_mcp = lm[0], lm[9]
    thumb_tip, index_tip = lm[4], lm[8]

    # palm size doubles as a "how close is the hand" ruler
    palm = distance(wrist, middle_mcp)

    return {
        # move your hand left/right -> base rotates
        "base": remap(wrist.x, 0.15, 0.85, *LIMITS["base"]),
        # y grows downwards, so the output range is flipped: hand up = arm up
        "shoulder": remap(wrist.y, 0.15, 0.85, LIMITS["shoulder"][1], LIMITS["shoulder"][0]),
        # hand closer to the camera = bigger palm = arm reaches further out
        "elbow": remap(palm, 0.10, 0.30, *LIMITS["elbow"]),
        # divided by palm so the pinch reads the same at any distance
        "gripper": remap(distance(thumb_tip, index_tip) / palm, 0.30, 1.60, *LIMITS["gripper"]),
    }


def draw_hud(frame, values, hand_found):
    for i, name in enumerate(JOINTS):
        y = 30 + i * 32
        low, high = LIMITS[name]
        filled = int(remap(values[name], low, high, 0, 200))
        cv2.rectangle(frame, (150, y - 12), (350, y + 6), (60, 60, 60), 1)
        cv2.rectangle(frame, (150, y - 12), (150 + filled, y + 6), (0, 200, 0), -1)
        cv2.putText(frame, f"{name:9s}{values[name]:3.0f}", (10, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    text, colour = ("TRACKING", (0, 255, 0)) if hand_found else ("NO HAND - arm holding", (0, 165, 255))
    cv2.putText(frame, text, (10, frame.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.7, colour, 2)


print("Starting camera... Press 'q' to quit, 'h' to send the arm home.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Mirror the image so moving your hand right moves the arm right
    frame = cv2.flip(frame, 1)
    result = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    hand_found = bool(result.multi_hand_landmarks)

    if hand_found:
        hand_landmarks = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        target = angles_from_hand(hand_landmarks)
        for name in JOINTS:
            # exponential smoothing: blend a little of the new value into the old one
            angles[name] += (target[name] - angles[name]) * SMOOTHING

    draw_hud(frame, angles, hand_found)

    now = time.time()
    rounded = {name: int(round(angles[name])) for name in JOINTS}
    moved = any(abs(rounded[n] - last_sent[n]) >= DEAD_BAND for n in JOINTS)

    # only publish when something actually moved, otherwise the broker floods
    if moved and now - last_send_time >= SEND_INTERVAL:
        client.publish(MQTT_TOPIC, ",".join(str(rounded[n]) for n in JOINTS))
        last_sent = rounded
        last_send_time = now

    cv2.imshow("Gesture Robot Arm Control", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    if key == ord('h'):  # panic button - straighten the arm back up
        angles = {"base": 90.0, "shoulder": 90.0, "elbow": 90.0, "gripper": 90.0}
        client.publish(MQTT_TOPIC, "90,90,90,90")
        last_sent = {n: 90 for n in JOINTS}

# Cleanup
cap.release()
cv2.destroyAllWindows()
client.loop_stop()
client.disconnect()
