# coding=utf-8
import cv2
import numpy as np
import random
import os
from argparse import ArgumentParser
ALPHA = 5





def main(ori, image):

    ori = ori
    img = image
    res = "./Blind_Watermark_results/"+"Decoded"+ori[9:]
    alpha = ALPHA
    if not os.path.isfile(ori):
        print("original image %s does not exist." % ori)
    if not os.path.isfile(img):
        print("image %s does not exist." % img)
    decode(ori, img, res, alpha)


def decode(ori_path, img_path, res_path, alpha):
    ori = cv2.imread(ori_path)
    img = cv2.imread(img_path)
    ori_f = np.fft.fft2(ori)
    img_f = np.fft.fft2(img)
    height, width = ori.shape[0], ori.shape[1]
    watermark = (ori_f - img_f) / alpha
    watermark = np.real(watermark)
    res = np.zeros(watermark.shape)
    random.seed(height + width)
    x = range(height // 2)
    y = range(width)
    random.shuffle(list(x))
    random.shuffle(list(y))
    for i in range(height // 2):
        for j in range(width):
            res[x[i]][y[j]] = watermark[i][j]
    cv2.imwrite(res_path, res, [int(cv2.IMWRITE_JPEG_QUALITY), 100])


if __name__ == '__main__':
    main()