import cv2
import numpy as np

draw = False
ix,iy = -1,-1

def circle_shape(event, x, y, flagval, par):
  if event == cv2.EVENT_LBUTTONDOWN:
      print(x,y)
      cv2.circle(image_window,(x,y),50,(255,0,0),-1)

def rectangle_shape (event, x,y,flagvar,par):
    global draw, ix,iy
    if event==cv2.EVENT_LBUTTONDOWN:
        draw = True
        ix, iy = x, y
    elif event==cv2.EVENT_MOUSEMOVE:
        if draw:
            cv2.rectangle(image_window,(ix,iy),(x,y),(255,0,0),1)
    elif event==cv2.EVENT_LBUTTONUP:
        draw = False
        cv2.rectangle(image_window,(ix,iy),(x,y),(255,0,0),1)
        print(f"({ix},{iy}),({x},{y})")

cv2.namedWindow(winname='Image_Window')
cv2.setMouseCallback('Image_Window',rectangle_shape)
image_window = np.zeros((720,720,3),np.uint8)

while True:
    cv2.imshow('Image_Window',image_window)
    if cv2.waitKey(1) & 0xFF == 27:
        break
cv2.destroyAllWindows()
