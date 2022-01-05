import sys
import cv2


# BER (in %) tra il watermark estratto e quello originale.
import numpy as np
from PIL import Image
img = Image.open('512-watermark.png').convert('RGBA')
arr = np.array(img)
# record the original shape
shape = arr.shape
# make a 1-dimensional view of arr
flat_arr = arr.ravel()
# convert it to a matrix
vector = np.matrix(flat_arr)
vector[:,::10] = 128
# reform a numpy array of the original shape
arr2 = np.asarray(vector).reshape(shape)
vector2=np.where(vector > 0, 1, vector)

immagine2 = Image.open('DWT-SVD-Mode1_cameraman.jpeg').convert('RGBA')
secondoarray = np.array(immagine2)
# record the original shape
shape2 = secondoarray.shape
# make a 1-dimensional view of arr
flat_arr2 = secondoarray.ravel()
# convert it to a matrix
vector3 = np.matrix(flat_arr2)
vector3[:,::10] = 128
# reform a numpy array of the original shape
secondoarray = np.asarray(vector3).reshape(shape2)
vector4=np.where(vector3 > 0, 1, vector3)

array1=np.concatenate(vector2, axis=0)
array2=np.concatenate(vector4, axis=0)


vector2=array1.tolist()
vector4=array2.tolist()



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

print(calcBER(vector2, vector4))