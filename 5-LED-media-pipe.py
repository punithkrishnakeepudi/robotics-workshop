import cv2
import mediapipe as mp
import paho.mqtt.client as mqtt

# MQTT Configuration
# Using a public broker for testing. 
# Make sure this matches the broker in your ESP8266 code.
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_TOPIC = "grrr_workshop/esp8266/led"

# Setup MQTT Client
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# MediaPipe Setup
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

cap = cv2.VideoCapture(0)

# To prevent flooding the MQTT broker, we keep track of the current LED state
current_state = "OFF"

def is_hand_open(hand_landmarks):
    # Tip landmarks: Index(8), Middle(12), Ring(16), Pinky(20)
    # PIP landmarks (joint below tip): Index(6), Middle(10), Ring(14), Pinky(18)
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    
    open_fingers = 0
    for tip, pip in zip(tips, pips):
        # In OpenCV, y coordinates increase downwards. 
        # If tip y is smaller than pip y, the finger is extended upwards.
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[pip].y:
            open_fingers += 1
            
    # If 3 or more fingers are extended, we consider the hand open
    return open_fingers >= 3

def is_hand_closed(hand_landmarks):
    tips = [8, 12, 16, 20]
    pips = [6, 10, 14, 18]
    
    closed_fingers = 0
    for tip, pip in zip(tips, pips):
        if hand_landmarks.landmark[tip].y > hand_landmarks.landmark[pip].y:
            closed_fingers += 1
            
    # If 3 or more fingers are closed, we consider the hand closed
    return closed_fingers >= 3

print("Starting camera... Press 'q' to quit.")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
        
    # Mirror the image for a more intuitive experience
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and get hand landmarks
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Check gesture
            if is_hand_open(hand_landmarks):
                cv2.putText(frame, "HAND OPEN - LED ON", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if current_state != "ON":
                    client.publish(MQTT_TOPIC, "ON")
                    current_state = "ON"
                    print("Detected Open Hand - Sent ON command")
                    
            elif is_hand_closed(hand_landmarks):
                cv2.putText(frame, "HAND CLOSED - LED OFF", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if current_state != "OFF":
                    client.publish(MQTT_TOPIC, "OFF")
                    current_state = "OFF"
                    print("Detected Closed Hand - Sent OFF command")
                    
    cv2.imshow("Hand Gesture LED Control", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
client.loop_stop()
client.disconnect()
