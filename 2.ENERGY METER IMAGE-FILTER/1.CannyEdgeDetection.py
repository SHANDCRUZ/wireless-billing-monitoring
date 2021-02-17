# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:43:59 2021

@author: SHANDCRUZ
"""
# `
import cv2

image = cv2.imread("source/ENERGYMETER.jpeg") 
gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
edged = cv2.Canny(image, 10, 250) 
cv2.imshow("edge", edged) 
cv2.waitKey(0)
cv2.destroyAllWindows() 
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
idx = 0 
for c in cnts: 
	x,y,w,h = cv2.boundingRect(c) 
	if w>400 and h>90: 
		idx+=1 
		new_img=image[y:y+h,x:x+w] 
		cv2.imwrite( 'source/canny'+str(idx)+'.png', new_img) 
cv2.imshow("im",new_img) 
cv2.waitKey(0) 
cv2.destroyAllWindows() 