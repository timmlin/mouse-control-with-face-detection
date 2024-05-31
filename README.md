# Wink Detection and Mouse Control

This Python script utilizes computer vision techniques with OpenCV to detect winks in real-time through a webcam. When a wink is detected, it can control the mouse cursor accordingly, allowing for hands-free interaction with the computer.

The clickCounter python file produces a basic TKinter GUI with a single button and a counter. This can be used to test the accuracy of the blink-to-click method.


## Table of Contents

- [Features](#Features)
- [Installation](#installation)
- [Usage](#usage)




## Features

* Detects winks from the user's left and right eye.
* Moves the mouse cursor 10 pixels to the left or right upon detecting a left or right wink, respectively.
* Detects blinks by identifying frames where only one eye is open.
* Includes a debounce timer to prevent a single blink from being registered multiple times.



## Getting Started
### Requirements
    

OpenCV

pyautogui

NumPy (usually included with OpenCV)

### Installation

Install the required libraries:
```
pip install opencv-python pyautogui
```



## Usage

Run the script:

``` bash
python wink_detection.py
```

### How It Works

The main loop continuously captures frames from the webcam, detects faces, and determines if one or both eyes are open.
If one eye is detected, the side of the open eye determines if the mouse moves left or right.
If no eyes are detected (a blink), a debounce timer ensures a single blink isn't registered multiple times.
If enough time has passed since the last blink, a left click is simulated using pyautogui.click().

### Notes

This code provides a basic example of wink detection and mouse control using OpenCV. It can be further customized and extended for more complex functionalities.

If the program is being run on MacOS the '0' in the below line may need to be changed to a '-1'      
```python
cap = cv2.VideoCapture(0)
```