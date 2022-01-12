import os
import cv2
import matplotlib.pyplot as plt
from DCT_DWT_SVD_watermarking_technique import functions as f
from textwrap import wrap
from os import listdir
from os.path import isfile, join

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
        plt.savefig('./Testing/Check_Diffs/Diffs.png', dpi = 100)
        plt.imshow(diff)
    plt.show()
