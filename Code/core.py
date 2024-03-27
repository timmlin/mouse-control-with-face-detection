"""
COSC428 Project - GUI navigation based on Eye movement

Author - Dipin P Joseph (ID-72746678)

Description - The project involves detection of face and eye and controls a GUI app with horizontal eye movement.

Usage - 3 Blinks to start the application and cursor will follows horizontal eye movements. Later on single blink to trigger UI buttons.

"""
# Importing necessary libraries
import numpy as np
import cv2
import dlib
import modules
import sys
from PyQt5.QtWidgets import *

# Declaration of global constants

# Threshold area, no.of frames considered for eye blink
EYE_AR_THRESH = 0.19
# To rule out accidental blinks
EYE_AR_CONSEC_FRAMES = 2
FONT = cv2.FONT_HERSHEY_TRIPLEX
# Flags for blink check and threshold definitions
DEF_FLAG = 0
FLAG_BLINK = 3
# Counter flag, total count for blink check
COUNTER = 0
TOTAL = 0
# Point indices for eyes in landmark data
LEFT_EYE_POINTS = [36, 37, 38, 39, 40, 41]
RIGHT_EYE_POINTS = [42, 43, 44, 45, 46, 47]
# Sum of non-zero points in first 10 frames
Sum_Q = (0,0)

# Aid application - PyQt5
app = QApplication([])
w = QWidget()
# GUI creation
modules.gui_init(w)

# Loading dlib frontal face detector (HOG-based) and landmark data.
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("Assets/shape_predictor_68_face_landmarks.dat")

# Input source - Webcam or video location
#cap = cv2.VideoCapture("Assets/3.mp4")
cap = cv2.VideoCapture(0)


while True:

    # Reading frames till EOF
    ret, frame = cap.read()
    if ret is False:
        break

    # Mask for received frame
    m_frame = np.zeros((500, 500, 3), np.uint8)

    # Image to Grayscale conversion
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale for face detection.

    # Face detection, argument 0 - removes upsampling
    dets = detector(gray, 0)

    for d in dets:

        # Blue box around face
        cv2.rectangle(frame,(d.left(),d.bottom()),(d.right(),d.top()),(255,0,0),2)

        # Landmark detection
        shape = predictor(gray, d)

        # Detect blinking by eye aspect ratio
        l_e_ratio = modules.get_blinking_ratio(LEFT_EYE_POINTS, shape)
        r_e_ratio = modules.get_blinking_ratio(RIGHT_EYE_POINTS, shape)
        ear = (l_e_ratio[0] + r_e_ratio[0]) / 2

        cv2.line(frame, l_e_ratio[1], l_e_ratio[2], (0, 255, 0), 1)
        cv2.line(frame, l_e_ratio[3], l_e_ratio[4], (0, 255, 0), 1)
        cv2.line(frame, r_e_ratio [1], r_e_ratio[2], (0, 255, 0), 1)
        cv2.line(frame, r_e_ratio[3], r_e_ratio[4], (0, 255, 0), 1)

        l_e_bound = modules.get_region(LEFT_EYE_POINTS, shape)
        r_e_bound = modules.get_region(RIGHT_EYE_POINTS, shape)
        cv2.polylines(frame, [l_e_bound], True, (0, 255, 255), 1)
        cv2.polylines(frame, [r_e_bound], True, (0, 255, 255), 1)

        # Increment counter if eye aspect ratio is below predefined value
        if ear < EYE_AR_THRESH:
            COUNTER += 1
        else:
            # If eye is closed for predefined no.of frames increase blink count
            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                TOTAL += 1
            # If eye is open reset counter.
            COUNTER = 0

        cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30), FONT, 1, (255, 0, 255), 2)

        # Observe first 10 frames to set non zero counts of two quadrants
        if (DEF_FLAG < 10):
            ratio = modules.get_gaze(cv2, frame, l_e_bound, r_e_bound, gray)
            Sum_Q = [sum(x) for x in zip(Sum_Q, ratio)]
            DEF_FLAG += 1
        elif (DEF_FLAG == 10):
            Avg_Q = [int(x / 10) for x in Sum_Q]
            modules.set_Q(Avg_Q)
            DEF_FLAG += 1

        # If total blink is 3 or more, gui app is triggered.
        if TOTAL >= 3:
            cv2.putText(frame, "APP Triggered", (350, 30), FONT, 1, (0, 0, 255), 2)
            modules.cursor_loc(0, 0)

            # Add click when there is a blink
            if TOTAL > FLAG_BLINK:
                modules.trigger_click()

            # Moving to next phase for frames without closed eyes
            else:
                # Generating ratio of white area of eye in each quadrant and moves cursor accordingly
                g_ratio = modules.get_gaze(cv2, frame, l_e_bound, r_e_bound, gray)
                cur = modules.cursor_move(g_ratio)
                modules.cursor_loc(cur[0],cur[1])

            FLAG_BLINK = TOTAL

        modules.pos_window(cv2, "Eye Detection and Tracking", frame, 300, 300)

    # Close the script when 'q' is pressed.
    if cv2.waitKey(10) & 0xFF == ord('q'):
        sys.exit()

# App normal exit
app.exec_()
cap.release()
cv2.destroyAllWindows()


