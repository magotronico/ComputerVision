import cv2
import mediapipe as mp
import pyautogui

def draw_finger_tag(frame, finger_name, finger_position):
    # Draw a rectangle around the finger position
    x, y = int(finger_position.x * frame.shape[1]), int(finger_position.y * frame.shape[0])
    cv2.rectangle(frame, (x - 15, y - 15), (x + 15, y + 15), (0, 255, 0), 2)

    # Add a text tag above the rectangle
    cv2.putText(frame, finger_name, (x - 10, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

def is_finger_raised(finger_landmark_base, finger_landmark_tip):
    up = finger_landmark_base.y > finger_landmark_tip.y
    # if up:
    #     print("finger up")
    return up

def main():
    # Initialize mediapipe for hand detection
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

    # Initialize the video capture with the DirectShow backend
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # Mirror the image horizontally
        frame = cv2.flip(frame, 1)

        # Convert the frame to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the frame using mediapipe
        results = hands.process(frame_rgb)

        # Check for hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # # Draw rectangles and tags for all landmarks
                # for idx, landmark in enumerate(hand_landmarks.landmark):
                #     landmark_name = f"{idx}"
                #     draw_finger_tag(frame, landmark_name, landmark)
                # draw_finger_tag(frame, "6", hand_landmarks.landmark[6])
                # draw_finger_tag(frame, "8", hand_landmarks.landmark[8])
                # # Draw rectangles and tags for finger positions
                # # draw_finger_tag(frame, "Thumb", hand_landmarks.landmark[4])
                # draw_finger_tag(frame, "Index", hand_landmarks.landmark[8])
                # draw_finger_tag(frame, "Pinky", hand_landmarks.landmark[20])
                
                # Detect if the fist is closed
                finger_closed = 0
                
                # Detect if front of hand is facing the camera
                if hand_landmarks.landmark[4].x <= hand_landmarks.landmark[17].x:
                    if hand_landmarks.landmark[3].x < hand_landmarks.landmark[4].x:
                        finger_closed += 1
                elif hand_landmarks.landmark[4].x > hand_landmarks.landmark[17].x:
                    if hand_landmarks.landmark[3].x > hand_landmarks.landmark[4].x:
                        finger_closed += 1
                if hand_landmarks.landmark[20].y >= hand_landmarks.landmark[18].y:
                    finger_closed += 1
                if hand_landmarks.landmark[8].y >= hand_landmarks.landmark[6].y:
                    finger_closed += 1
                if hand_landmarks.landmark[12].y >= hand_landmarks.landmark[10].y:
                    finger_closed += 1
                if hand_landmarks.landmark[16].y >= hand_landmarks.landmark[14].y:
                    finger_closed += 1

                cv2.putText(frame, f"Finger closed: {finger_closed}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                
                if finger_closed == 4:
                    fist_closed = True
                else:
                    fist_closed = False

                # Detect if the index finger is raised
                index_finger_raised = is_finger_raised(hand_landmarks.landmark[6], hand_landmarks.landmark[8])

                # Detect if the pinky is raised
                pinky_raised = is_finger_raised(hand_landmarks.landmark[18], hand_landmarks.landmark[20])

                # # Display the finger status
                # cv2.putText(frame, f"Index raised: {index_finger_raised}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 2)
                # cv2.putText(frame, f"Pinky raised: {pinky_raised}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 150, 200), 2)
            
            # Adjust volume based on hand gesture
            if fist_closed:
                if index_finger_raised:
                    pyautogui.press('volumeup')
                elif pinky_raised:
                    pyautogui.press('volumedown')

        # Display the frame
        cv2.imshow('Hand Gesture Volume Control', frame)

        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break

    # Release video capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
