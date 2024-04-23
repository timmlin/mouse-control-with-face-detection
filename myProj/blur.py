import cv2
import sys



cap = cv2.VideoCapture(0)

while(cv2.waitKey(10) < 0):
    ret, img = cap.read()

    # Convert the rgb image to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Applying bilateral filters to remove impurities
    gray = cv2.bilateralFilter(gray, 30, 30, 30)

    
    cv2.imshow("default_image", img)
    cv2.imshow("grayscale/blur", gray)


cap.release()
cv2.destroyAllWindows()

