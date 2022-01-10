import cv2
import numpy as np
from PIL import Image

def main(watermark):

    watermark = cv2.imread(watermark, 0)
    watermark = cv2.resize(watermark, (512, 512))
    cv2.imwrite("./Watermark/512-watermark.png", watermark)
    filename= "./Watermark/512-watermark.png"
    img = Image.open( filename )
    data = np.array( img, dtype='uint8' )
    np.save('./Watermark/watermark.npy', data)


