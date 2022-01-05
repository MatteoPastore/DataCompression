import cv2
import numpy as np
from PIL import Image

def main():
    filename = '../Watermark/watermark.png'
    watermark = cv2.imread(filename, 0)
    watermark = cv2.resize(watermark, (32, 32))
    cv2.imwrite("watermark.png", watermark)
    filename="watermark.png"
    img = Image.open( filename )
    data = np.array( img, dtype='uint8' )
    np.save('watermark.npy', data)

