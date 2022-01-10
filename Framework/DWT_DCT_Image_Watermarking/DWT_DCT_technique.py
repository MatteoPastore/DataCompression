import numpy as np
import pywt
import os
from PIL import Image
from scipy.fftpack import dct
from scipy.fftpack import idct
import cv2

current_path = str(os.path.dirname(__file__))


#Modificato da PIL a cv2 poichè diceva che le immagini fossero corrotte e non poteva aprirle, siamo passati da una shape di immagine a colori ad una di immagine in scala di grigi. Il risultato è identico poichè cv2.imread apre l'immagine come un nparray, mentre usando PIL andava fatta la conversione a nparray
def convert_image(image_name, size):

    img = cv2.imread(image_name)
    dim=(size, size)
    img = cv2.resize(img, dim)
    img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    image_array=img



    return image_array


def process_coefficients(imArray, model, level):
    coeffs = pywt.wavedec2(data=imArray, wavelet=model, level=level)
    # print coeffs[0].__len__()
    coeffs_H = list(coeffs)

    return coeffs_H


def embed_mod2(coeff_image, coeff_watermark, offset=0):
    for i in range(coeff_watermark.__len__()):
        for j in range(coeff_watermark[i].__len__()):
            coeff_image[i * 2 + offset][j * 2 + offset] = coeff_watermark[i][j]

    return coeff_image


def embed_mod4(coeff_image, coeff_watermark):
    for i in range(coeff_watermark.__len__()):
        for j in range(coeff_watermark[i].__len__()):
            coeff_image[i * 4][j * 4] = coeff_watermark[i][j]

    return coeff_image


def embed_watermark(watermark_array, orig_image):
    watermark_array_size = watermark_array[0].__len__()
    watermark_flat = watermark_array.ravel()
    ind = 0

    for x in range(0, orig_image.__len__(), 8):
        for y in range(0, orig_image.__len__(), 8):
            if ind < watermark_flat.__len__():
                subdct = orig_image[x:x + 8, y:y + 8]
                subdct[5][5] = watermark_flat[ind]
                orig_image[x:x + 8, y:y + 8] = subdct
                ind += 1

    return orig_image


def apply_dct(image_array):
    size = image_array[0].__len__()
    all_subdct = np.empty((size, size))
    for i in range(0, size, 8):
        for j in range(0, size, 8):
            subpixels = image_array[i:i + 8, j:j + 8]
            subdct = dct(dct(subpixels.T, norm="ortho").T, norm="ortho")
            all_subdct[i:i + 8, j:j + 8] = subdct

    return all_subdct


def inverse_dct(all_subdct):
    size = all_subdct[0].__len__()
    all_subidct = np.empty((size, size))
    for i in range(0, size, 8):
        for j in range(0, size, 8):
            subidct = idct(idct(all_subdct[i:i + 8, j:j + 8].T, norm="ortho").T, norm="ortho")
            all_subidct[i:i + 8, j:j + 8] = subidct

    return all_subidct


def get_watermark(dct_watermarked_coeff, watermark_size):
    subwatermarks = []

    for x in range(0, dct_watermarked_coeff.__len__(), 8):
        for y in range(0, dct_watermarked_coeff.__len__(), 8):
            coeff_slice = dct_watermarked_coeff[x:x + 8, y:y + 8]
            subwatermarks.append(coeff_slice[5][5])

    watermark = np.array(subwatermarks).reshape(watermark_size, watermark_size)

    return watermark


def recover_watermark(imname, image_array, model='haar', level=1):
    coeffs_watermarked_image = process_coefficients(image_array, model, level=level)
    dct_watermarked_coeff = apply_dct(coeffs_watermarked_image[0])

    watermark_array = get_watermark(dct_watermarked_coeff, 128)

    watermark_array = np.uint8(watermark_array)

    # Save result
    img = Image.fromarray(watermark_array)
    img.save('./DWT_DCT_Image_Watermarking_results/Extracted/'+"DWT-DCT_"+imname+'.jpeg')


def print_image_from_array(image_array, name, image):
    image_array_copy = image_array.clip(0, 255)
    image_array_copy = image_array_copy.astype("uint8")
    img = Image.fromarray(image_array_copy)
    img.save(name)
    img.save("./imagesToAttack/"+"DWT-DCT_" + image)


def w2d(image, watermark):
    print(image[9:])
    imname=image[9:-5]
    model = 'haar'
    level = 1
    image_array = convert_image(image, 2048)
    watermark_array = convert_image(watermark, 128)

    coeffs_image = process_coefficients(image_array, model, level=level)
    dct_array = apply_dct(coeffs_image[0])
    dct_array = embed_watermark(watermark_array, dct_array)
    coeffs_image[0] = inverse_dct(dct_array)

    # reconstruction
    res = "./DWT_DCT_Image_Watermarking_results/Watermarked/" + "DWT-DCT_" + image[9:]
    img=image[9:]
    image_array_H = pywt.waverec2(coeffs_image, model)
    print_image_from_array(image_array_H, res, img)

    # recover images
    recover_watermark(imname, image_array=image_array_H, model=model, level=level)


