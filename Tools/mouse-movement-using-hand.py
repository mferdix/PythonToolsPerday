import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)

# Initialize OpenCV for video capture
cap = cv2.VideoCapture(0)

# Get screen resolution for cursor positioning
screen_width, screen_height = pyautogui.size()

while True:
    # Capture video frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to access the camera.")
        break

    # Flip the frame horizontally for better user experience (optional)
    frame = cv2.flip(frame, 1)
    
    # Convert the frame to RGB (MediaPipe uses RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame to find hands
    results = hands.process(rgb_frame)
    
    # Check if hands are detected
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw hand landmarks (optional, just for visualization)
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Get the position of the index finger (landmark 8)
            index_finger = hand_landmarks.landmark[8]
            index_x = int(index_finger.x * screen_width)
            index_y = int(index_finger.y * screen_height)

            # Move the cursor to the position of the index finger
            pyautogui.moveTo(index_x, index_y)

    # Display the frame with landmarks (optional)
    cv2.imshow("Hand Tracking", frame)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
