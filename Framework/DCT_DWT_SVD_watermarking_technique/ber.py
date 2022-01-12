import sys
import cv2
from PIL import Image
import numpy as np
import cv2
from DCT_DWT_SVD_watermarking_technique import attacks
import glob, os, os.path

def toBMP(watermarked):
    #Watermarked
    img=cv2.imread(watermarked)
    img=cv2.resize(img, (512, 512))
    cv2.imwrite("./Testing/Ber/"+watermarked[17:], img)
    img = Image.open('./Testing/Ber/'+watermarked[17:])
    ary = np.array(img)

    # Split the three channels
    r,g,b = np.split(ary,3,axis=2)
    r=r.reshape(-1)
    g=r.reshape(-1)
    b=r.reshape(-1)

    # Standard RGB to grayscale
    bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2],
    zip(r,g,b)))
    bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((bitmap > 128).astype(float),255)
    im = Image.fromarray(bitmap.astype(np.uint8))

    im.save("./Testing/Ber/"+watermarked[17:])



    img = cv2.imread("./Testing/Ber/"+watermarked[17:], 0)
    _, ImageBit = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)
    imgList=ImageBit.tolist()


    #Original
    imageName = watermarked.split('_')[1]
    if imageName[-4:]== ".bmp":
        img = cv2.imread("./originalImages/" + imageName[:-4]+".jpeg")
    else:
        img = cv2.imread("./originalImages/" + imageName)

    img = cv2.resize(img, (512, 512))
    cv2.imwrite("./Testing/Ber/" + imageName, img)

    img = Image.open("./Testing/Ber/" + imageName)
    ary = np.array(img)

    # Split the three channels
    r,g,b = np.split(ary,3,axis=2)
    r=r.reshape(-1)
    g=r.reshape(-1)
    b=r.reshape(-1)

    # Standard RGB to grayscale
    bitmap = list(map(lambda x: 0.299*x[0]+0.587*x[1]+0.114*x[2],
    zip(r,g,b)))
    bitmap = np.array(bitmap).reshape([ary.shape[0], ary.shape[1]])
    bitmap = np.dot((bitmap > 128).astype(float),255)
    watermark = Image.fromarray(bitmap.astype(np.uint8))
    watermark.save('./Testing/Ber/'+imageName)

    img = cv2.imread('./Testing/Ber/'+imageName, 0)
    _, watermarkBit = cv2.threshold(img, 127, 1, cv2.THRESH_BINARY)
    watermarkList=watermarkBit.tolist()

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

def main(image):

    algorithmName = image.split('_')[0]
    imageName = image.split('_')[1]



    data1, data2 = toBMP(image)

    ber = calcBER(data1, data2)
    print("Bit error ratio between " + imageName + " watermarked with " + algorithmName[17:] + " and original is ")
    print(ber)
    algorithmNames = algorithmName[17:]
    saveThis = [imageName, algorithmNames, ber]
    attacks.append_list_as_row('./Testing/Ber/Ber.csv', saveThis)

    filelist = glob.glob(os.path.join("./Testing/Ber", "*.bmp"))
    for f in filelist:
        os.remove(f)
    filelist = glob.glob(os.path.join("./Testing/Ber", "*.jpeg"))
    for f in filelist:
        os.remove(f)
