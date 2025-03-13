import cv2
import mediapipe as mp
import pyautogui
# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
index_x, index_y = 0, 0
thumb_x, thumb_y = 0, 0
frame_count = 0  # Counter to skip frames
frame_skip = 5  # Number of frames to skip
click_threshold = 30  # Adjust as needed
while True:
    _, frame = cap.read()
    frame_count += 1
    if frame_count % frame_skip == 0:
        frame_count = 0  # Reset frame count
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x * frame_width)
                    y = int(landmark.y * frame_height)
                    if id == 8:
                        index_x = screen_width / frame_width * x
                        index_y = screen_height / frame_height * y
                    if id == 4:
                        thumb_x = screen_width / frame_width * x
                        thumb_y = screen_height / frame_height * y
                        # scroll up Gesture
                        if thumb_y < index_y - 50:
                            pyautogui.scroll(50)  # Increase scroll amount
                            print("scroll up")
                        # scroll down Gesture
                        elif thumb_y > index_y + 50:
                            pyautogui.scroll(-50)  # Decrease scroll amount
                            print("scroll down")
                        # Click Gesture
                        if abs(index_x - thumb_x) < click_threshold and abs(index_y - thumb_y) < click_threshold:
                            pyautogui.click()
                            print("Click")
        pyautogui.moveTo(index_x, index_y)
    cv2.imshow('Virtual Mouse', frame)
    cv2.waitKey(1)
