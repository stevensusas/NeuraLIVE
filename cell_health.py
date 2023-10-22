import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import glob
import os
# classify cell types

def classify_cells(image_name):
    img = cv.imread(image_name)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv.threshold(gray, 130, 255, cv.THRESH_BINARY)
    # cv.imshow('Grayscaled image', thresh)

    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    circle = 0
    ellipse = 0

    for contour in contours:
        # Approximate the contour
        epsilon = 0.04 * cv.arcLength(contour, True)
        approx = cv.approxPolyDP(contour, epsilon, True)

        # Calculate the aspect ratio
        x, y, _, _ = cv.boundingRect(contour)
        
        if (len(approx) < 6 and len(approx) > 3):
            shape = 'Ellipse'
            ellipse += 1
            cv.drawContours(img, [contour], 0, (0, 0, 255), 2)
            cv.putText(img, shape, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 200), 2)
        elif len(approx) > 5:
            shape = 'Circle'
            circle += 1
            cv.drawContours(img, [contour], 0, (0, 255, 0), 2)
            cv.putText(img, shape, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 200, 0), 2)

    circle = int(circle/3)
    ellipse = int(ellipse/3)
    health = ellipse/(ellipse+circle) * 100
    return circle, ellipse, health


def generate_graphs(graphpath,graphname):
    
    image_files = glob.glob(os.path.join(graphpath,'*.tif'))
    circle_results = [[], [], [], []]
    ellipse_results = [[], [], [], []]
    health_rate = [[], [], [], []]
    
    

    # Extract image number from filenames
    image_numbers = [int(''.join(filter(lambda x: x in '0123456789', image_file.split('_')[7]))) for image_file in image_files]
    image_culture_numbers = [int(''.join(filter(lambda x: x in '0123456789', image_file.split('_')[8]))) for image_file in image_files]
   
    # Sort the iamge files based on the image number 
    sorted_image_files = [x for _, x in sorted(zip(image_numbers, zip(image_files, image_culture_numbers)))]

    for image_file, image_culture_number in sorted_image_files:
        circle, ellipse, health = classify_cells(image_file)
        if (image_culture_number in [1, 2, 3, 4]):
            circle_results[image_culture_number-1].append(circle)
            ellipse_results[image_culture_number-1].append(ellipse)
            health_rate[image_culture_number-1].append(health)

    # plot results for each culture
    plt.scatter(range(0, len(circle_results[0])), circle_results[0], marker='o', s=30, c='r', label='Rep 1 Unadhered Cells')
    plt.scatter(range(0, len(ellipse_results[0])), ellipse_results[0], marker='^', s=30, c='r', label='Rep 1 Adhered Cells')
    plt.scatter(range(0, len(circle_results[1])), circle_results[1], marker='o', s=30, c='g', label='Rep 2 Unadhered Cells')
    plt.scatter(range(0, len(ellipse_results[1])), ellipse_results[1], marker='^', s=30, c='g', label='Rep 2 Adhered Cells')
    plt.scatter(range(0, len(circle_results[2])), circle_results[2], marker='o', s=30, c='b', label='Rep 3 Unadhered Cells')
    plt.scatter(range(0, len(ellipse_results[2])), ellipse_results[2], marker='^', s=30, c='b', label='Rep 3 Adhered Cells')
    plt.scatter(range(0, len(circle_results[3])), circle_results[3], marker='o', s=30, c='y', label='Rep 4 Unadhered Cells')
    plt.scatter(range(0, len(ellipse_results[3])), ellipse_results[3], marker='^', s=30, c='y', label='Rep 4 Adhered Cells')

    plt.xlabel('Time')
    plt.ylabel('Counts of Adhered & Unadhered Cells')
    plt.title('Cell Adherence')
    plt.grid(True)
    plt.legend()
    graph_filename = 'static/' + graphname + 'types.png'
    plt.savefig(graph_filename)
    plt.close()

    # plot cell health rate for each culture

    plt.plot(range(0, len(health_rate[0])), health_rate[0], c='r', label='Rep 1')
    plt.plot(range(0, len(health_rate[1])), health_rate[1], c='g', label='Rep 2')
    plt.plot(range(0, len(health_rate[2])), health_rate[2], c='b', label='Rep 3')
    plt.plot(range(0, len(health_rate[3])), health_rate[3], c='y', label='Rep 4')

    plt.xlabel('Time')
    plt.ylabel('Percentage of Healthy Cells')
    plt.title('Cell Health')
    plt.grid(True)
    plt.legend()
    graph_filename = 'static/' + graphname + 'rate.png'
    plt.savefig(graph_filename)
    plt.close()

generate_graphs('extracted_files/SHSY5Y_Rep_1/SHSY5Y Rep 1','1')