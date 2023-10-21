from torchvision.transforms import ToTensor
import cv2 as cv
import rasterio
from rasterio.plot import show
import numpy as np
from matplotlib import pyplot as plt

path = "./SHSY5Y_Phase_B10_1_00d04h00m_4.tif"

#with rasterio.open(path) as image:
#    image_array = image.read() # numpy.ndarray h w c

img = cv.imread(path)
dst = cv.fastNlMeansDenoising(img)
a = dst

plt.subplot(121),plt.imshow(img)
plt.subplot(122),plt.imshow(dst)

for h in a:
    for w in h:
        for c in w:
            if c == 126 or c == 127 or c == 128 or c == 129 or c == 130 or c == 131: 
                a[h,w] = 256
            else:
                print(c)

plt.subplot(221),plt.imshow(a)
plt.show()

# branch is horizontal
#def decideBranch(x, y, count):
    # if pixel.isBackground:
        # mark red
       # return
    #if (count == 3):
        # mark red
    #    return
  #  decideBranch(pixel.left, count+1)
  #  decideBranch(pixel.right, count+1)



torch_image = ToTensor()(dst)
print(torch_image.shape)
show(dst)


