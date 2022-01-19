import os
import cv2
import matplotlib.pyplot as plt
from DCT_DWT_SVD_watermarking_technique import functions as f
from textwrap import wrap
from os import listdir
from os.path import isfile, join
from skimage.metrics import structural_similarity
import numpy as np

def imageOnFolder(mypath) :
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def main():

    imagesToAttack = imageOnFolder('./imagesToAttack/')
    i = 0


    for path in imagesToAttack:
        thisImageResults = []
        groupName = path.split('_')[0]
        imageName = path.split('_')[1]

        if imageName[-4:] == ".bmp":
            originalPath = "./originalImages/" + str(imageName[:-4] + ".jpeg")

        else:
            originalPath = "./originalImages/" + imageName


        watermarkedPath = "./imagesToAttack/" + str(path)

        watermarked = cv2.imread(watermarkedPath, 0)


        print(f'Testing image n°{i+1}, {imageName} of the group {groupName} ')

        original = cv2.imread(originalPath, 0)
        original = cv2.resize(original, (512, 512))


        watermarked = cv2.imread(watermarkedPath, 0)
        watermarked = cv2.resize(watermarked, (512, 512))


        diff = original - watermarked


        i += 1

        plt.subplot(11, 18, i)
        plt.title(f'{imageName}_{groupName}', fontsize=5)
        plt.imshow(diff)
        plt.savefig('./Testing/Check_Diffs/Diffs.png', dpi=100)

        #plt.show()
####################################################
# Compute SSIM between two images
        (score, diff) = structural_similarity(original, watermarked, full=True)
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

        mask = np.zeros(original.shape, dtype='uint8')
        filled_after = watermarked.copy()

        for c in contours:
            area = cv2.contourArea(c)
            if area > 40:
                x, y, w, h = cv2.boundingRect(c)
                cv2.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), 2)
                cv2.rectangle(watermarked, (x, y), (x + w, y + h), (36, 255, 12), 2)
                cv2.drawContours(mask, [c], 0, (0, 255, 0), -1)
                cv2.drawContours(filled_after, [c], 0, (0, 255, 0), -1)

        #cv2.imshow('before', original)
        #cv2.imshow('after', watermarked)
        #cv2.imshow('diff', diff)
        #cv2.imshow('mask', mask)
        #cv2.imshow('filled after', filled_after)
        #cv2.waitKey(0)




        differencesPlot = np.concatenate((original, watermarked, diff))

        #cv2.imwrite("./Testing/Ber/plotDiffs/Diffs_" + input5 + "_" + input4[:-4] + ".png", diff)
        cv2.imwrite("./Testing/Check_Diffs/Diffs_" + groupName + "_" + imageName[:-4] + ".png", differencesPlot*255)