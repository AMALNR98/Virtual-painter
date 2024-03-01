import cv2
import numpy as np

import HandTrackingModule as htm

detector = htm.handDetector()
draw_color = (255,255,255)

# Creating image canvas
img_canvas = np.zeros((720, 1280,3),np.uint8)


cap = cv2.VideoCapture(0)

# while True:
#     x,frame = cap.read()
#     cv2.imshow('Virtual painter', frame)
#     if cv2.waitKey(1) & 0xFF == 27:
#         break
#     cap.release


while True:
    x,img = cap.read()
    img = cv2.resize(img,(1280,720))
    img = cv2.flip(img, 1)
    # Draw rectangles
    img = cv2.rectangle(img,(10,100),(200,10),(255,0,0),-1)
    img = cv2.rectangle(img,(210,100),(400,10),(0,255,0),-1)
    img = cv2.rectangle(img,(420,100),(600,10),(0,0,255),-1)   
    img = cv2.rectangle(img,(620,100),(800,10),(0,255,255),-1)
    img = cv2.rectangle(img,(820,100),(1270,10),(255,255,255),-1)
    img = cv2.putText(img, text='Eraser',
                      org=(1000,60),
                      fontFace=cv2.FONT_HERSHEY_COMPLEX,
                      fontScale=1,
                      color=(0,0,0),
                      thickness=3
                      )
    # Detect hands
    img = detector.findHands(img)
    # Take positions
        # Create an landmark list
    lmlist = detector.findPosition(img)

    # print(lmlist)


    # take values form lmlist
    if len(lmlist)!=0:
        x1, y1 = lmlist[8][1:] # index finger tip coordinates
        x2, y2 = lmlist[12][1:] # middle finger tip coordinates

        # print("x1 and y1 are",x1,y1)
        # print("x2 and y2 are",x1,y1)

# Detect if fingers are up
        fingers = detector.fingersUp()
        # print(fingers)

# Check if twos fingers are up - selection mode
        if fingers[1] and fingers[2]:
            # print('Selection mode')

            # Generate previous mode points
            xp,yp = 0,0
            
            if y1 < 100:
                if 10 <= x1 <=200:
                    # print('Blue')
                    draw_color = (255,0,0)

                elif 210 <= x1 <=400:
                    # print('Green')
                    draw_color = (0,255,0)

                elif 420 <= x1 <= 600:
                    # print("Red")
                    draw_color = (0,0,255)

                elif 620 <= x1 <= 800:
                    # print("Yellow")
                    draw_color = (0,255,255)

                elif 820 <= x1 <= 1270:
                    draw_color = (0,0,0)
                    # print("Eraser")

            cv2.rectangle(img,(x1,y1),(x2,y2),color=draw_color,thickness=-1)


# Check if index index finger is up - drawing mode
        if fingers[1] and not  fingers[2]:
            print('drawing mode')   
            cv2.circle(img,(x1,y1),15, draw_color,thickness=-1)
            
            if xp == 0 and yp == 0:
                xp = x1
                yp = y1
            # colors
            if draw_color == (0,0,0):
                cv2.line(img,[xp,yp],[x1,y1],color=draw_color,thickness=50)
                cv2.line(img_canvas,[xp,yp],[x1,y1],color=draw_color,thickness=50)

            else:
                cv2.line(img,[xp,yp],[x1,y1],color=draw_color,thickness=15)
                cv2.line(img_canvas,[xp,yp],[x1,y1],color=draw_color,thickness=15)
           
            xp,yp = x1,y1
            

# Merging canvas and video
    # converting img canvas to grayscale
    img_gray = cv2.cvtColor(img_canvas,cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(img_gray,20,255,cv2.THRESH_BINARY_INV)
    # conveting this gray image to bgr 
    img_inv = cv2.cvtColor(img_inv,cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img,img_inv)
    img = cv2.bitwise_or(img, img_canvas)

    # Adding images
    img = cv2.addWeighted(img,1,img_canvas,0.5,0)

    cv2.imshow('Virtual painter', img)
    # cv2.imshow('Virtual painter canvas', img_canvas)

    if cv2.waitKey(1) & 0xFF == 27:
        break
    cap.release


# Detect if fingers are up
    
# Check if twos fingers are up - selection mode
    
# Check if index index finger is up - drawing mode