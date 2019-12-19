import os
import cv2
import numpy as np
import sys

image = cv2.imread('1.jpeg')

# print(image)


img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

ret, mask = cv2.threshold(image, 100, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)


green = np.uint8([[[255,0,0 ]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print(hsv_green)

# sys.exit()
lower_blue = np.array([110, 100, 100])
upper_blue = np.array([130,255,255])

mask = cv2.inRange(image, lower_blue, upper_blue)

# Bitwise-AND mask and original image
res = cv2.bitwise_and(image,image, mask= mask)

cv2.imshow('frame',image)
cv2.imshow('mask',mask)
cv2.imshow("res",res)


cv2.waitKey(0)
cv2.destroyAllWindows()

