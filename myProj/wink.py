import cv2
import sys
import pyautogui
import time

blink_timer = 0

def moveMouse(right):
    if right:
        pyautogui.move(10, 0)
    else:
        pyautogui.move(-10, 0)


def blink():
    pyautogui.click()


def detectWink(frame, location, ROI, eye_cascade, right=False):

    x_r , _ = ROI.shape
    eyes = eye_cascade.detectMultiScale(ROI, 1.04, 15, minSize = (5, 10))

    for (ex,ey,ew,eh) in eyes:
        ex += location[0]
        ey += location[1]

        if right:
            x_r = int(x_r*7/8)

            cv2.rectangle(frame, (ex + x_r, ey), (ex + ew + x_r, ey + eh), (0, 255, 255), 2)
        else:
            cv2.rectangle(frame, (ex, ey), (ex+ew, ey+eh), (0, 255, 255), 2)
    return len(eyes)>0   



if __name__ == "__main__":

    #Face and eye cascade classifiers from xml files
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_eye.xml')

    blinkCount = 0
    cap = cv2.VideoCapture(0)
    loop = 0
    while(cv2.waitKey(10) < 0):

       # start_time = time.time()
    
        ret, img = cap.read()

        # Convert the rgb image to gray
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Applying bilateral filters to remove impurities
        gray = cv2.bilateralFilter(gray, 5, 1, 1)

        scaleFactor = 1.02 
        minNeighbors = 5 
        minSize = (200,200) 

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor,
            minNeighbors,
            minSize = minSize)
        
        
        for (x,y,w,h) in faces:

            left_roi_face = gray[y:int(y+(h*1/2)), x:x+int(w*1/2)]
            right_roi_face = gray[y:int(y+(h*1/2)), x+int(w*1/2):(x+w)]

            eyeCount = 0
            
            left_eye = detectWink(img, (x, y), left_roi_face, eye_cascade)
            right_eye = detectWink(img, (x, y), right_roi_face, eye_cascade,right=True)

            
            eyeCount = left_eye + right_eye

            if eyeCount == 1:


                if left_eye:
                    cv2.rectangle(img, (x,y), (x+w,y+h), (255, 0, 0), 2)
                    cv2.putText(img,'Left Wink detected',(int(x+(w/8)) ,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2,cv2.LINE_AA)
                    moveMouse(right = False)
                elif right_eye:
                    cv2.rectangle(img, (x,y), (x+w,y+h), (255, 0, 0), 2)
                    cv2.putText(img, 'Right Wink detected',(int(x+(w/8)) ,y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,(255,255,255),2,cv2.LINE_AA)
                    moveMouse(right = True)

            elif eyeCount == 0:
                
                #tacks the last time the blink function was called to 
                #prevent one blink being counted as multiple
                current_time = time.time()
                if current_time - blink_timer >= 0.5:
                    blink()
                    blink_timer = current_time


            else:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0, 255, 0), 2)

        # end_time = time.time()
        # elapsed_time = end_time - start_time
        # print(f"Time taken: {elapsed_time:.2f} seconds")
        cv2.imshow("wink_detection", img)


    cap.release()
    cv2.destroyAllWindows()