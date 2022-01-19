import sys
import cv2
from PIL import Image
import numpy as np
import cv2
from DCT_DWT_SVD_watermarking_technique import attacks
import glob, os, os.path
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity
import cv2
import numpy as np
import io


def toBMP(img1, img2, input4, input5, iteration, attacco):

    img1=cv2.resize(img1, (512, 512))
    #cv2.imwrite("./Testing/Ber/"+input5+"_"+input4, 0)


    _, ImageBit = cv2.threshold(img1, 127, 1, cv2.THRESH_BINARY)
    imgList=ImageBit.tolist()




    img2 = cv2.resize(img2, (512, 512))
    #cv2.imwrite("./Testing/Ber/attacked_"+input5+"_"+input4, 0)

    _, watermarkBit = cv2.threshold(img2, 127, 1, cv2.THRESH_BINARY)
    watermarkList=watermarkBit.tolist()

    #Creazione file differenze immagini concatenate
    differences = cv2.hconcat([img1, img2])

    cv2.imwrite("./Testing/Ber/differences/beforeAfter_"+input5+"_"+input4[:-4]+".jpeg", differences*255)




##############################


    # Compute SSIM between two images
    (score, diff) = structural_similarity(img1, img2, full=True)
    print("Image similarity", score)

    # The diff image contains the actual image differences between the two images
    # and is represented as a floating point data type in the range [0,1]
    # so we must convert the array to 8-bit unsigned integers in the range
    # [0,255] before we can use it with OpenCV
    diff = (diff * 255).astype("uint8")

    # Threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]

    mask = np.zeros(img1.shape, dtype='uint8')
    filled_after = img2.copy()

    for c in contours:
        area = cv2.contourArea(c)
        if area > 40:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(img1, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.rectangle(img2, (x, y), (x + w, y + h), (36, 255, 12), 2)
            cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
            cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

    #cv2.imshow('before', img1)s
    #cv2.imshow('after', img2)
    #cv2.imshow('diff', diff)
    #cv2.imshow('mask', mask)
    #cv2.imshow('filled after', filled_after)
    #cv2.waitKey(0)



    differencesPlot = np.concatenate((img1, img2, diff))
    path="./Testing/Ber/plotDiffs/" + input5 + "_" + input4[:-4] + " Iterazione "+str(iteration)+ " Attacco "+str(attacco)+".png"
    #print(path)
    cv2.imwrite(path, diff)
    #cv2.imwrite("./Testing/Ber/plotDiffs/Diffs_" + input5 + "_" + input4[:-4] + ".png", differencesPlot*255)


################################

    if len(imgList) != len(watermarkList):
        print('The input data have different length.')
        print('Please give data with the same length.')
        sys.exit()

    error_bits = 0
    for (d1, d2) in zip(imgList, watermarkList):
        if d1 != d2:
            error_bits += 1

    data_len = len(imgList)
    # ber definito come il numero di bit diversi nel watermark estratto rispetto l'originale / il numero di bit del watermark originale
    ber = (error_bits / data_len) * 100

    return ber






def main(img1, img2, input4, input5, iteration, attacco):





    ber = toBMP(img1, img2, input4, input5, iteration, attacco)


    print("Bit error ratio between watermark and attackedWatermark is ")
    print(ber)

    saveThis = [input4, input5, ber, attacco, iteration]
    attacks.append_list_as_row('./Testing/Ber/Ber.csv', saveThis)

    filelist = glob.glob(os.path.join("./Testing/Ber", "*.bmp"))
    for f in filelist:
        os.remove(f)
    filelist = glob.glob(os.path.join("./Testing/Ber", "*.jpeg"))
    for f in filelist:
        os.remove(f)
