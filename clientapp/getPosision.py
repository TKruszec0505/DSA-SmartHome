import pyautogui
import mediapipe as mp
import cv2
#from mediapipe.tasks import python
#from mediapipe.tasks.python import vision


runingtrack = False
def run_main():
    TARGET_WIDTH = 3840
    TARGET_HEIGHT = 1080

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=2,
                           min_detection_confidence=0.5,
                           min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)

    global runingtrack
    runingtrack = True

    while runingtrack:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)  # Lustro
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)
        frame_timestamp_ms = cap.get(cv2.CAP_PROP_POS_MSEC)

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        #recognizer.recognize_async(mp_image, int(frame_timestamp_ms))
        if result.multi_hand_landmarks and result.multi_handedness:
            for hand_landmarks, hand_handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                label = hand_handedness.classification[0].label
                if label == 'Left':
                    print("")
                if label == 'Right':  # Tylko prawa ręka
                    klik_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]

                    dx = int(klik_finger_tip.x * w)
                    dy = int(klik_finger_tip.y * h)

                    dscreen_x = int(klik_finger_tip.x * TARGET_WIDTH)
                    dscreen_y = int(klik_finger_tip.y * TARGET_HEIGHT)

                    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

                    # Współrzędne palca
                    cx = int(index_finger_tip.x * w)
                    cy = int(index_finger_tip.y * h)

                    screen_x = int(index_finger_tip.x * TARGET_WIDTH)
                    screen_y = int(index_finger_tip.y * TARGET_HEIGHT)

                    # Debug info
                    print(f"Palec: x={screen_x}, y={screen_y}" + f"kciuk: x={dscreen_x}, y={dscreen_y}")
                    cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
                    cv2.putText(frame, f"{screen_x}, {screen_y}", (cx, cy - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                    cv2.circle(frame, (dx, dy), 10, (0, 255, 0), -1)
                    cv2.putText(frame, f"{dscreen_x}, {dscreen_y}", (dx, dy - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                    pyautogui.moveTo(screen_x, screen_y)
                    if dscreen_x - screen_x < 100 and dscreen_y - screen_y < 100:
                        pyautogui.mouseDown(button='left')
                        print("test zrealizowano pomyslnie")
                    else:
                        pyautogui.mouseUp(button='left')

        cv2.imshow("Finger Tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()