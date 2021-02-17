# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:50:17 2021

@author: SHANDCRUZ
"""
import cv2

im = cv2.imread("source/monocropped.jpg")
j = int((im.shape[1])/7)
h = int(im.shape[0])
z=0
for i in range(0,7):
    crop = im[0:92 , z:z+j]   
    crop =cv2.resize(crop,(224,224))
    cv2.imwrite('source/ '+str(i)+".jpg",crop)
    z+=j
    cv2.imshow("crop"+str(i),crop)
    cv2.waitKey(0)

cv2.destroyAllWindows() 