import cv2
import mediapipe as mp
import screen_brightness_control as sbc

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

def recognize_gesture(hand_landmarks):
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    
    
    current = sbc.get_brightness(display=0)[0]


    if thumb_tip.y > index_tip.y:
        sbc.set_brightness(display=0, value=min(100, current + 10))
    else:
        sbc.set_brightness(display=0, value=max(0, current - 10))

hands = mp_hands.Hands(
    static_image_mode=False,       
    max_num_hands=2,              
    min_detection_confidence=0.5,  
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)

while True :
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            x = hand_landmarks.landmark[8].x
            y = hand_landmarks.landmark[8].y
            h, w, _ = frame.shape
            cx, cy = int(x * w), int(y * h)
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            gesture = recognize_gesture(hand_landmarks)
            cv2.putText(frame, gesture, (cx - 50, cy - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    cv2.imshow("Hand Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()