import cv2
import mediapipe as mp
import pyautogui
import time
# Disable PyAutoGUI fail-safe
pyautogui.FAILSAFE = False
class EyeTracker:
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
        self.screen_w, self.screen_h = pyautogui.size()
        # Constants for eye landmarks
        self.LEFT_EYE_LANDMARKS = [33, 133, 155, 157, 159, 161, 163, 173]
        self.RIGHT_EYE_LANDMARKS = [362, 384, 386, 388, 390, 392, 402, 447]
        # Variables for cursor control
        self.prev_x, self.prev_y = None, None
        self.cursor_speed = 5  # Adjust as needed
        self.blink_threshold = 0.02  # Adjust dynamically based on testing
        self.frame_rate = 60  # Adjust based on camera capabilities
        self.delay = int(1000 / self.frame_rate)  # Delay in milliseconds to achieve desired frame rate
    def track_eyes(self):
        frame_count = 0
        start_time = time.time()
        while True:
            _, frame = self.cam.read()
            frame_count += 1
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            output = self.face_mesh.process(rgb_frame)
            landmark_points = output.multi_face_landmarks
            frame_h, frame_w, _ = frame.shape
            if landmark_points:
                landmarks = landmark_points[0].landmark
                left_eye_x = left_eye_y = right_eye_x = right_eye_y = None
                # Calculate the average position of the left eye landmarks
                for landmark_index in self.LEFT_EYE_LANDMARKS:
                    x, y = landmarks[landmark_index].x, landmarks[landmark_index].y
                    left_eye_x = x if left_eye_x is None else (left_eye_x + x) / 2
                    left_eye_y = y if left_eye_y is None else (left_eye_y + y) / 2
                # Calculate the average position of the right eye landmarks
                for landmark_index in self.RIGHT_EYE_LANDMARKS:
                    x, y = landmarks[landmark_index].x, landmarks[landmark_index].y
                    right_eye_x = x if right_eye_x is None else (right_eye_x + x) / 2
                    right_eye_y = y if right_eye_y is None else (right_eye_y + y) / 2
                # Calculate the average eye position
                eye_x = (left_eye_x + right_eye_x) / 2
                eye_y = (left_eye_y + right_eye_y) / 2
                if self.prev_x is not None and self.prev_y is not None:
                    # Calculate the cursor movement based on the difference
                    move_x = (eye_x - self.prev_x) * self.screen_w * self.cursor_speed
                    move_y = (eye_y - self.prev_y) * self.screen_h * self.cursor_speed
                    # Move the cursor with smoothing
                    pyautogui.move(move_x, move_y, duration=0.2)
                # Store the current eye position as the previous position
                self.prev_x, self.prev_y = eye_x, eye_y
                # Check for a blink
                blink_distance = abs(left_eye_y - right_eye_y)
                if blink_distance > self.blink_threshold:
                    pyautogui.click()
                    pyautogui.sleep(1)
            # Display the frame
            cv2.imshow('Eye-Controlled Mouse', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            # Delay to achieve the desired frame rate
            cv2.waitKey(self.delay)
            if frame_count % 30 == 0:  # Print frame rate every 30 frames
                elapsed_time = time.time() - start_time
                actual_frame_rate = frame_count / elapsed_time
                print(f"Actual Frame Rate: {actual_frame_rate:.2f} fps")
        self.cam.release()
        cv2.destroyAllWindows()
if __name__ == "__main__":
    eye_tracker = EyeTracker()
    eye_tracker.track_eyes()
