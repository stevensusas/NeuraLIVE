from skimage.filters import frangi, hessian, sato, meijering
from skimage import io
import matplotlib.pyplot as plt
import cv2
import glob
import numpy as np
import os

# image = cv2.imread('./SHSY5Y_Phase_B10_1_00d04h00m_4.tif')


#plt.figure(figsize=(10, 5))

# Display the original image
#plt.subplot(1, 2, 1)
#plt.imshow(image, cmap='gray')
#plt.title('Original Image')
#plt.axis('off')

# Display the filtered image
#plt.subplot(1, 2, 2)
#plt.imshow(filtered_image, cmap='gray')
#plt.title('Filtered Image (Frangi)')
#plt.axis('off')
#plt.show()



def count_branches(image_file):
    image = cv2.imread(image_file, cv2.IMREAD_COLOR)
    greyscale = cv2. cvtColor(image, cv2.COLOR_BGR2GRAY)
    dns_greyscale = cv2.fastNlMeansDenoising(greyscale)
    filtered_image  = meijering(dns_greyscale, [1], black_ridges = True)
    
    return np.sum((filtered_image > 5/255) & (filtered_image < 0.045))


def generate_branch_plot(graphpath, image_name):
    # Process the images
    image_files = glob.glob(os.path.join(graphpath,'*.tif'))
    # image_files = glob.glob('./SHSY5Y_Rep1/*.tif')
    results = [[],[],[],[]]

    # Extract image numbers from filenames
    #image_numbers = [int(''.join(filter(lambda x: x in '0123456789', image_file.split('_')[5]))) for image_file in image_files]
    #image_culture_numbers = [int(''.join(filter(lambda x: x in '0123456789', image_file.split('_')[6]))) for image_file in image_files]
    image_numbers = [int(''.join(filter(lambda x: x in '0123456789', image_file.split('_')[7]))) for image_file in image_files]
    image_culture_numbers = [int(''.join(filter(lambda x: x in '0123456789', image_file.split('_')[8]))) for image_file in image_files]
    
    # Sort the image files based on the image number
    sorted_image_files = [x for _, x in sorted(zip(image_numbers, zip(image_files, image_culture_numbers)))]

    for image_file, image_culture_number in sorted_image_files:
        num_branches = count_branches(image_file)
        if (image_culture_number in [1, 2, 3, 4]):
            results[image_culture_number-1].append(num_branches)



    plt.scatter(range(1, len(results[0]) + 1), results[0], marker='o', s=30, c='b', label='Rep 1')
    plt.scatter(range(1, len(results[1]) + 1), results[1], marker='o', s=30, c='r', label='Rep 2')
    plt.scatter(range(1, len(results[2]) + 1), results[2], marker='o', s=30, c='g', label='Rep 3')
    plt.scatter(range(1, len(results[3]) + 1), results[3], marker='o', s=30, c='c', label='Rep 4')
    plt.xlabel('Time')
    plt.ylabel('Number of red pixels')
    plt.title('Cell Branches')
    plt.grid(True)
    plt.legend()
    graph_filename = 'static/' + image_name + 'types.png'
    plt.savefig(graph_filename)
    plt.show()
    plt.close()