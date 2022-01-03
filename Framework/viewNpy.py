
from PIL import Image
from numpy import asarray
import cv2

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

filename = './Images/Lenna.jpeg'
watermark = cv2.imread(filename, 0)
watermark = cv2.resize(watermark, (32, 32))
cv2.imwrite("watermark.jpeg", watermark)
filename="watermark.jpeg"
img = Image.open( filename )
data = np.array( img, dtype='uint8' )

np.save( 'watermark.npy', data)

# visually testing our output
#img_array = np.load(filename + '.npy')
from matplotlib import pyplot as plt

#plt.imshow(img_array, cmap='gray')
#plt.show()