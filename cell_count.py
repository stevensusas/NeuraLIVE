import cv2
import numpy as np
import glob
import matplotlib.pyplot as plt

# Function to count cells based on their shape
def count_cells(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    threshold_value = 130 # Adjust this value
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)
    cv2.imshow('Binary Image', thresh)
    # Find contours in the thresholded image
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cell_count = 0
    for contour in contours:
        # Approximate the contour as a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        # Check if the contour is almost circular or a bulge (e.g., having a certain number of vertices)
        if len(approx) >= 7:
            cell_count += 1

    return cell_count

