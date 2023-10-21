import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('SHSY5Y_Phase_B10_1_00d04h00m_2.tif')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
plt.imshow(thresh, cmap='gray')
plt.axis('off')  
plt.show()
