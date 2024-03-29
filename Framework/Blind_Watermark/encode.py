# coding=utf-8
import cv2
import numpy as np
import random
import os
from argparse import ArgumentParser
ALPHA = 5

#Il codice originale prevedeva l'inserimento degli input tramite riga di comando
#Lo abbiamo modificato in modo che prenda gli input da "launchAll"

def main(image, watermark):

    img = image
    print(image[9:])
    wm = watermark
    res = "./Blind_Watermark_results/Watermarked/"+"DFT_"+img[9:]
    pathAttack = "./imagesToAttack/" + "DFT_" + img[9:]
    alpha = ALPHA
    if not os.path.isfile(img):
        print("image %s does not exist." % img)
    if not os.path.isfile(wm):
        print("watermark %s does not exist." % wm)
    encode(img, wm, res, alpha, pathAttack)
    return res


def encode(img_path, wm_path, res_path, alpha, pathAttack):
    img = cv2.imread(img_path)
    #La funzione "fft.fft2" effettua una trasformata discreta di Fourier bidimensionale
    img_f = np.fft.fft2(img)
    height, width, channel = np.shape(img)
    watermark = cv2.imread(wm_path)
    wm_height, wm_width = watermark.shape[0], watermark.shape[1]
    #print(type(height), type(width))

    x, y = range(height // 2), range(width)
    random.seed(height + width)
    random.shuffle(list(x))
    random.shuffle(list(y))
    tmp = np.zeros(img.shape)
    for i in range(height // 2):
        for j in range(width):
            if x[i] < wm_height and y[j] < wm_width:
                tmp[i][j] = watermark[x[i]][y[j]]
                tmp[height - 1 - i][width - 1 - j] = tmp[i][j]
    res_f = img_f + alpha * tmp
    res = np.fft.ifft2(res_f)
    res = np.real(res)
    cv2.imwrite(res_path, res, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

    cv2.imwrite(pathAttack, res, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
if __name__ == '__main__':
    main()