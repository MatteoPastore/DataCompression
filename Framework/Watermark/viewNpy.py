import cv2
import numpy as np
from PIL import Image


filename = 'watermark.png'
watermark = cv2.imread(filename, 0)
watermark = cv2.resize(watermark, (32, 32))
cv2.imwrite("32-watermark.png", watermark)
filename="32-watermark.png"
img = Image.open( filename )
data = np.array( img, dtype='uint8' )
np.save('watermark.npy', data)

