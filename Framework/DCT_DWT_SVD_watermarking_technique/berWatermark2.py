import sys
import cv2
from PIL import Image
import numpy as np
import cv2
from DCT_DWT_SVD_watermarking_technique import attacks
import glob, os, os.path

def toBMP(img1, img2):

    img1=cv2.resize(img1, (512, 512))

    _, ImageBit = cv2.threshold(img1, 127, 1, cv2.THRESH_BINARY)
    imgList=ImageBit.tolist()


    #Original


    img2 = cv2.resize(img2, (512, 512))

    _, watermarkBit = cv2.threshold(img2, 127, 1, cv2.THRESH_BINARY)
    watermarkList=watermarkBit.tolist()
    #cv2.imshow("a",img1)

    #cv2.imshow("b",img2)
    cv2.waitKey(0)


    return imgList, watermarkList



def calcBER(data1, data2):
    if len(data1) != len(data2):
        print('The input data have different length.')
        print('Please give data with the same length.')
        sys.exit()

    error_bits = 0
    for (d1, d2) in zip(data1, data2):
        if d1 != d2:

            error_bits += 1

    data_len = len(data1)
    #ber definito come il numero di bit diversi nel watermark estratto rispetto l'originale / il numero di bit del watermark originale
    ber = (error_bits / data_len) * 100

    return ber

def main(img1, img2, input4, input5):





    data1, data2 = toBMP(img1, img2)

    ber = calcBER(data1, data2)
    print("Bit error ratio between watermark and attackedWatermark is ")
    print(ber)

    saveThis = [input4, input5, ber]
    attacks.append_list_as_row('./Testing/Ber/Ber.csv', saveThis)

    filelist = glob.glob(os.path.join("./Testing/Ber", "*.bmp"))
    for f in filelist:
        os.remove(f)
    filelist = glob.glob(os.path.join("./Testing/Ber", "*.jpeg"))
    for f in filelist:
        os.remove(f)
