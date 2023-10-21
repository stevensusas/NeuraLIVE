import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
img = cv.imread('SHSY5Y_Phase_B10_1_00d04h00m_2.tif')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

i=0
circle = 0
ellipse = 0

for contour in contours:
    # Approximate the contour
    epsilon = 0.04 * cv.arcLength(contour, True)
    approx = cv.approxPolyDP(contour, epsilon, True)

    # Calculate the aspect ratio
    x, y, w, h = cv.boundingRect(contour)
    aspect_ratio = float(w) / h
    
    # Check aspect ratio to distinguish between circle and ellipse
    if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
        shape = "Circle"
        circle += 1
    else:
        shape = "Ellipse"
        ellipse += 1

    # Draw the contour and label the shape
    cv.drawContours(img, [contour], 0, (0, 0, 255), 2)
    cv.putText(img, shape, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

print(circle, "circles")
print(ellipse, "ellipses")
# Display the result
# plt.imshow(thresh, cmap='Greys')
plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
plt.axis('off')
plt.show()