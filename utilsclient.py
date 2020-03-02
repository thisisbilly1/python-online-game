# -*- coding: utf-8 -*-
import cv2
import numpy as np
font=cv2.FONT_HERSHEY_SIMPLEX

def makeinfowindow(ping):
    img=np.ones((25,200,3),np.uint8)*255
    img = cv2.putText(img, str(ping),(5,17),font, .5, (0,0,0), 1, cv2.LINE_AA)
    return img