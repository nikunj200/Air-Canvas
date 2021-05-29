import numpy as np
import cv2
from collections import deque

def setValues(x):
    print("")

cap = cv2.VideoCapture(0)

class Canvas:
    def __init__(self):
        self.bpoints = [deque(maxlen=1024)]
        self.gpoints = [deque(maxlen=1024)]
        self.rpoints = [deque(maxlen=1024)]
        self.ypoints = [deque(maxlen=1024)]

        self.blue_index = 0
        self.green_index = 0
        self.red_index = 0
        self.yellow_index = 0

        self.kernel = np.ones((5,5), np.uint8)

        self.colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
        self.colorIndex = 0

        self.__init__paintWindow()

    def __init__paintWindow(self):
        self.paintWindow = np.zeros((720, 900, 3)) + 255
        self.paintWindow = cv2.rectangle(self.paintWindow, (40,1), (140,65), (0,0,0), 2)
        self.paintWindow = cv2.rectangle(self.paintWindow, (160,1), (255,65), self.colors[0], -1)
        self.paintWindow = cv2.rectangle(self.paintWindow, (275,1), (370,65), self.colors[1], -1)
        self.paintWindow = cv2.rectangle(self.paintWindow, (390,1), (485,65), self.colors[2], -1)
        self.paintWindow = cv2.rectangle(self.paintWindow, (505,1), (600,65), self.colors[3], -1)

        cv2.putText(self.paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(self.paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)

    def processCapture(self, frame):
        #Flipping the frame to see same side of yours
        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        Upper_hsv = np.array([153, 255, 255])
        Lower_hsv = np.array([64, 72, 49])

        # Adding the colour buttons to the live frame for colour access
        frame = cv2.rectangle(frame, (40,1), (140,65), (122,122,122), -1)
        frame = cv2.rectangle(frame, (160,1), (255,65), self.colors[0], -1)
        frame = cv2.rectangle(frame, (275,1), (370,65), self.colors[1], -1)
        frame = cv2.rectangle(frame, (390,1), (485,65), self.colors[2], -1)
        frame = cv2.rectangle(frame, (505,1), (600,65), self.colors[3], -1)
        cv2.putText(frame, "CLEAR ALL", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150,150,150), 2, cv2.LINE_AA)


        # Identifying the pointer by making its mask
        Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
        Mask = cv2.erode(Mask, self.kernel, iterations=1)
        Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, self.kernel)
        Mask = cv2.dilate(Mask, self.kernel, iterations=1)

        # Find contours for the pointer after idetifying it
        cnts,_ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        center = None

        # Ifthe contours are formed
        if len(cnts) > 0:
            # sorting the contours to find biggest 
            cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
            # Get the radius of the enclosing circle around the found contour
            ((x, y), radius) = cv2.minEnclosingCircle(cnt)
            # Draw the circle around the contour
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            # Calculating the center of the detected contour
            M = cv2.moments(cnt)
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

            # Now checking if the user wants to click on any button above the screen 
            if center[1] <= 65:
                if 40 <= center[0] <= 140: # Clear Button
                    self.bpoints = [deque(maxlen=512)]
                    self.gpoints = [deque(maxlen=512)]
                    self.rpoints = [deque(maxlen=512)]
                    self.ypoints = [deque(maxlen=512)]

                    self.blue_index = 0
                    self.green_index = 0
                    self.red_index = 0
                    self.yellow_index = 0

                    self.paintWindow[67:,:,:] = 255
                elif 160 <= center[0] <= 255:
                        self.colorIndex = 0 # Blue
                elif 275 <= center[0] <= 370:
                        self.colorIndex = 1 # Green
                elif 390 <= center[0] <= 485:
                        self.colorIndex = 2 # Red
                elif 505 <= center[0] <= 600:
                        self.colorIndex = 3 # Yellow
            else :
                if self.colorIndex == 0:
                    self.bpoints[self.blue_index].appendleft(center)
                elif self.colorIndex == 1:
                    self.gpoints[self.green_index].appendleft(center)
                elif self.colorIndex == 2:
                    self.rpoints[self.red_index].appendleft(center)
                elif self.colorIndex == 3:
                    self.ypoints[self.yellow_index].appendleft(center)
        # Append the next deques when nothing is detected to avois messing up
        else:
            self.bpoints.append(deque(maxlen=512))
            self.blue_index += 1
            self.gpoints.append(deque(maxlen=512))
            self.green_index += 1
            self.rpoints.append(deque(maxlen=512))
            self.red_index += 1
            self.ypoints.append(deque(maxlen=512))
            self.yellow_index += 1

        # Draw lines of all the colors on the canvas and frame 
        points = [self.bpoints, self.gpoints, self.rpoints, self.ypoints]
        for i in range(len(points)):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None:
                        continue
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], self.colors[i], 2)
                    cv2.line(self.paintWindow, points[i][j][k - 1], points[i][j][k], self.colors[i], 2)
        self.frame = frame

    def get_paintWindow(self):
        return self.paintWindow
    
    def get_frame(self):
        return self.frame

canvas = Canvas()
