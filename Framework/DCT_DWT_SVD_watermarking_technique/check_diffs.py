import os
import cv2
import matplotlib.pyplot as plt
import functions as f
from textwrap import wrap


imagesToAttack = f.imageOnFolder('../imagesToAttack/')
i = 0

for path in imagesToAttack:
    thisImageResults = []
    groupName = path.split('_')[0]
    imageName = path.split('_')[1]
    originalPath = "../originalImages/" + str(imageName[:-4] +".jpeg")
    watermarkedPath = "../imagesToAttack/" + str(path)
    watermarked = cv2.imread(watermarkedPath, 0)


    print(f'Testing {imageName} of the group {groupName}...')

    original = cv2.imread(originalPath, 0)


    watermarked = cv2.imread(watermarkedPath, 0)
    diff = original.astype(int) - watermarked
    i += 1
    plt.subplot(2, 10, i)
    plt.title(f'{imageName}_{groupName}', fontsize=5)
    plt.imshow(diff)
plt.show()
