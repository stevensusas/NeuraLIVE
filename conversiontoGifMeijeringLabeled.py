from skimage.filters import frangi, hessian, sato, meijering
import matplotlib.pyplot as plt
import cv2
import numpy as np
import glob
from PIL import Image
import imageio
import os

def generateMejerinRedLabel(inputimage):
    image =  cv2.imread(inputimage)
    image_m =  cv2.imread(inputimage)
    greyscale_m = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dns_greyscale_m = cv2.fastNlMeansDenoising(greyscale_m)

    meijering_filtered_image  = meijering(dns_greyscale_m, [1], black_ridges = True)

    image_m[((meijering_filtered_image > 2/255) & (meijering_filtered_image < 0.05))] = (255, 0, 0)

    lower_red = np.array([255, 0, 0])
    upper_red = np.array([255, 0, 0])

    red_mask = cv2.inRange(image_m, lower_red, upper_red)
    return image_m

def createSortedCellImageArray(path):
    image_files = glob.glob(os.path.join(path,'*.tif'))
    image_numbers = [int(''.join(filter(lambda x: x in '0123456789', image_file.split('_')[7]))) for image_file in image_files]
# Sort the image files based on the image number
    sorted_image_files = [x for _, x in sorted(zip(image_numbers, image_files))]
    return sorted_image_files

#takes an array of sorted .tif images as the input
def createPlainCellGiffromObject(sorted_image_object,id):
    frame_duration = 200 
        # Extract image numbers from filenames

    images = []

    for x in sorted_image_object:
        images.append(x)

    
    # Save the list of images as a GIF at a given location
    imageio.mimsave('static/GIFlabelled'+id+'.gif', images, duration=frame_duration / 1000.0)

