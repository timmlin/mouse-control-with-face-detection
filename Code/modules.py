""""
Collection of different utility methods needed for the Project.
"""
# Loading necessary libraries
import numpy as np
import sys
from math import hypot
from functools import partial
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
import pyautogui

# Center point of GUI application
CURSOR_X = 1000
CURSOR_Y = 150
# Declaration of global constants
THRESHOLD = 50
MULTIPLIER = 5

QP = 140,108
h_pos = 0
v_pos = 0

def alert_msg(info,w):
    """
    Method to initiate click response
    :param info:
    """
    msg = QLabel(w)
    msg.setAutoFillBackground(1)
    msg.setText(info)
    msg.setFixedWidth(300)
    msg.setFont(QtGui.QFont("Times", 12, QtGui.QFont.Bold))
    msg.setAlignment(Qt.AlignCenter)
    msg.move(250, 130)
    msg.show()

def gui_init(w):
    """
    Method to create initial GUI
    :param w: window object
    :return:
    """
    fb = QPushButton('Food and\n Beverages', w)
    fb.move(50, 25)
    fb.clicked.connect(partial(alert_msg,"Request sent to Service Desk.",w))
    fb.setStyleSheet("font: bold;background-color: #00ff55;font-size: 18px; width: 100px; height: 80px")
    me = QPushButton('Medical\n Emergency', w)
    me.move(200, 25)
    me.clicked.connect(partial(alert_msg,"Critical assistance requested.",w))
    me.setStyleSheet("font: bold;background-color: #b30000;font-size: 18px; width: 100px; height: 80px")
    ent = QPushButton('Movies', w)
    ent.move(350, 25)
    ent.clicked.connect(partial(alert_msg,"Requested service will be available shortly.",w))
    ent.setStyleSheet("font: bold;background-color: #ffcc00;font-size: 18px; width: 100px; height: 80px")
    te = QPushButton('Teleservices', w)
    te.move(500, 25)
    te.clicked.connect(partial(alert_msg,"Connection request placed.",w))
    te.setStyleSheet("font: bold;background-color: #4da6ff;font-size: 18px; width: 100px; height: 80px")
    ext = QPushButton('Exit', w)
    ext.move(650, 25)
    ext.clicked.connect(sys.exit)
    ext.setStyleSheet("font: bold;background-color: #b30000;font-size: 18px; width: 100px; height: 80px")

    w.setGeometry(600, 100, 800, 170)
    w.setWindowTitle('AID App')
    w.setStyleSheet("background-color: #e6e6e6;")
    w.show()

def midpoint(p1 ,p2):
    """
    Utility method to get vertical mmidpoint of eye
    :param p1: Point 1
    :param p2: Point 2
    :return: Midpoint
    """
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2)

def get_blinking_ratio(eye_points, shape):
    """
    Method to find vertical and horizontal distance of an eye.
    :param eye_points:
    :param shape:
    :return: Ratio between eye vertical and eye horizontal distances
    """
    l_point = (shape.part(eye_points[0]).x, shape.part(eye_points[0]).y)
    r_point = (shape.part(eye_points[3]).x, shape.part(eye_points[3]).y)
    c_top = midpoint(shape.part(eye_points[1]), shape.part(eye_points[2]))
    c_bottom = midpoint(shape.part(eye_points[5]), shape.part(eye_points[4]))

    hl_length = hypot((l_point[0] - r_point[0]), (l_point[1] - r_point[1]))
    vl_length = hypot((c_top[0] - c_bottom[0]), (c_top[1] - c_bottom[1]))

    ear = vl_length / hl_length

    return (ear, l_point, r_point, c_top, c_bottom)

def get_region(eye_points, shape):
    """
    Method to find points of each eye frame from shape
    :param eye_points: Landmarks points of eye
    :param shape: dlib eye object
    :return:
    """
    e_region = np.array([(shape.part(eye_points[0]).x, shape.part(eye_points[0]).y),
                                (shape.part(eye_points[1]).x, shape.part(eye_points[1]).y),
                                (shape.part(eye_points[2]).x, shape.part(eye_points[2]).y),
                                (shape.part(eye_points[3]).x, shape.part(eye_points[3]).y),
                                (shape.part(eye_points[4]).x, shape.part(eye_points[4]).y),
                                (shape.part(eye_points[5]).x, shape.part(eye_points[5]).y)], np.int32)
    return (e_region)

def get_gaze(cv2, frame, l_e_bound, r_e_bound, gray):
    """
    Method to find out denisty of white area on both eyes
    :param cv2: Opencv Object
    :param frame: Frame under consideration
    :param l_e_bound: Left eye points
    :param r_e_bound: Right eye points
    :param gray: Grayscaled frame
    :return: Sum of white area of both eyes
    """
    height, width, _ = frame.shape
    mask = np.zeros((height, width), np.uint8)
    cv2.polylines(mask, [l_e_bound,r_e_bound], True, 255, 2)
    cv2.fillPoly(mask, [l_e_bound,r_e_bound], 255)
    eye = cv2.bitwise_and(gray, gray, mask=mask)
    #pos_window(cv2, "Masked - Eye", eye, 0, 600)
    #cv2.imshow("Masked - Eye",eye)

    l_threshold = get_threshold(l_e_bound, eye, cv2)
    r_threshold = get_threshold(r_e_bound, eye, cv2)

    pos_window(cv2, "Masked - Left Eye Threshold", l_threshold, 1200, 400)
    pos_window(cv2, "Masked - Right Eye Threshold", r_threshold, 1200,600)
    #cv2.imshow("Masked - Left Eye Threshold", l_threshold)
    #cv2.imshow("Masked - Right Eye Threshold", r_threshold)

    l_gaze = get_density(l_threshold, cv2)
    r_gaze = get_density(r_threshold, cv2)
    gaze = [sum(x) for x in zip(l_gaze,r_gaze)]
    #v_split = (gaze[0]+gaze[2])/(gaze[1]+gaze[3]+0.00000000000000001)
    #h_split = (gaze[0] + gaze[1]) / (gaze[2] + gaze[3]+0.00000000000000001)
    #return(h_split, v_split)

    return(gaze)

def get_threshold(e_bound, eye, cv2):
    """
    Convert eye to black and white points based on given threshold value
    :param e_bound: Eye points on frame
    :param eye: masked eye region
    :param cv2: Opencv object
    :return: Eye after threshold operation
    """

    min_x = np.min(e_bound[:, 0])
    max_x = np.max(e_bound[:, 0])
    min_y = np.min(e_bound[:, 1])
    max_y = np.max(e_bound[:, 1])

    gray_eye = eye[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(gray_eye, THRESHOLD, 255, cv2.THRESH_BINARY)

    return (threshold_eye)

def get_density(threshold_eye, cv2):
    """
    Method to divide eye to two quadrants and finds white area of each
    :param threshold_eye: Eye object after threshold operation
    :param cv2: Opencv object
    :return: Area of white region
    """

    height, width = threshold_eye.shape

    #q0 = cv2.countNonZero(threshold_eye[int(height/2): height, 0: int(width / 2)])
    #q1 = cv2.countNonZero(threshold_eye[int(height/2): height, int(width / 2): width])
    #q2 = cv2.countNonZero(threshold_eye[0: int(height/2), 0: int(width / 2)])
    #q3 = cv2.countNonZero(threshold_eye[0: int(height/2), int(width / 2): width])
    q0 = cv2.countNonZero(threshold_eye[0: height, 0: int(width / 2)])
    q1 = cv2.countNonZero(threshold_eye[0: height, int(width / 2): width])

    #return (q0,q1,q2,q3)
    return (q0,q1)


def pos_window(cv2, name, img, x, y):
    """
    Utility method to create and move new windows
    :param cv2: Opencv object
    :param name: WIndow name
    :param img: Frame
    :param x: X co-ordinate
    :param y: Y co-ordinate
    """
    cv2.namedWindow(name)
    cv2.moveWindow(name, x, y)
    cv2.imshow(name,img)

def cursor_move(Q):
    """
    Utility method to find necessary movement according to the eye position
    :param Q: White area of current frame
    :return: Change in position of cursor
    """
    global QP,h_pos,v_pos

    try:
        ratio = ([x / y for x, y in zip(Q, QP)])

        if(abs(ratio[0]-ratio[1]) > 0.8):

            (max_q_val, max_q) = max((v, i) for i, v in enumerate(ratio))
            if max_q == 0:
                h_pos, v_pos = -1*MULTIPLIER, 0
            else:
                h_pos, v_pos = 1*MULTIPLIER, 0

        else:
            h_pos, v_pos = 0, 0

    except Exception as e:
        h_pos, v_pos = 0,0
        print("Exception : ",e)

    return(h_pos, v_pos)

def set_Q(Q):
    """
    Method to set default quadrant values based on first 10  frames
    :param Q: Average values of first 10 frames
    """
    global QP
    QP = Q

def trigger_click():
    """
    Trigger mouse click.
    """
    pyautogui.click()

def cursor_loc(x,y):
    """
    Method to move cursor along the screen according to the params
    :param x: X co-ordinate
    :param y: Y co-ordinate
    :return:
    """
    global CURSOR_X,CURSOR_Y
    CURSOR_X += x
    CURSOR_Y += y
    pyautogui.moveTo(CURSOR_X,CURSOR_Y)