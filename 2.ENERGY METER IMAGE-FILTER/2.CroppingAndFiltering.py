# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:47:59 2021

@author: SHANDCRUZ
"""
from PIL import Image
import cv2

image_file = Image.open("source/canny1.png") # open colour image
image_file = image_file.convert('L') # convert image to black and white
image_file = image_file.convert('L')
image_file.save('source/result.png')
img = cv2.imread('source/result.png')
x=0
img1 =img[60:152, 4:361]
cv2.imshow("show",img1)
print(img1.shape)
cv2.imwrite("source/monocropped.jpg",img1)
cv2.waitKey(0)
cv2.destroyAllWindows()

# checking the commit 3
