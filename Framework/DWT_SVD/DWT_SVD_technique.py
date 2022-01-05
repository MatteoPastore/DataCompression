# -*- coding: utf-8 -*-
# @Time    : 14/04/2017 14:46
# @Author  : Luke
# @Software: PyCharm

import cv2
import pywt
import numpy as np




class Components():
    Coefficients = []
    U = None
    S = None
    V = None


class watermarking():
    """
    :param watermark_path:
    :param ratio:
    :param wavelet:
    :param level:
    """
    def __init__(self, watermark_path, ratio=0.1, wavelet="haar",
                 level=2):

        self.level = level
        self.wavelet = wavelet
        self.ratio = ratio
        self.shape_watermark = cv2.imread(watermark_path, 0).shape
        self.W_components = Components()
        self.img_components = Components()
        self.W_components.Coefficients, self.W_components.U, \
        self.W_components.S, self.W_components.V = self.calculate(watermark_path)


    def calculate(self, img):
        '''
        To calculate the Coefficients and SVD components.
        :param img: should be a numpy array or the path of the image.
        '''
        if isinstance(img, str):
            img = cv2.imread(img, 0)
        Coefficients = pywt.wavedec2(img, wavelet=self.wavelet, level=self.level)
        self.shape_LL = Coefficients[0].shape
        U, S, V = np.linalg.svd(Coefficients[0])
        return Coefficients, U, S, V

    def diag(self, s):
        '''
        To recover the singular values to be a matrix.
        :param s: a 1D numpy array
        '''
        S = np.zeros(self.shape_LL)
        row = min(S.shape)
        S[:row, :row] = np.diag(s)
        return S

    def recover(self, name):
        '''
        To recover the image from the svd components and DWT
        :param name:
        '''
        components = eval("self.{}_components".format(name))
        s = eval("self.S_{}".format(name))
        components.Coefficients[0] = components.U.dot(self.diag(s)).dot(components.V)
        return pywt.waverec2(components.Coefficients, wavelet=self.wavelet)

    def watermark(self, img, path_save=None):
        '''
        This is the main function for image watermarking.
        :param img: image path or numpy array of the image.
        '''

        if not path_save:
            path_save = "./DWT_SVD_resultsMode1/Watermarked/DWT-SVD-Mode1_" + img[16:]

        self.path_save = path_save
        self.img_components.Coefficients, self.img_components.U, \
        self.img_components.S, self.img_components.V = self.calculate(img)
        self.embed()
        img_rec = self.recover("img")
        cv2.imwrite(path_save, img_rec)

    def extracted(self, image_path=None, ratio=None, extracted_watermark_path = None):
        '''
        Extracted the watermark from the given image.
        '''

        if not extracted_watermark_path:

            extracted_watermark_path = "./DWT_SVD_resultsMode1/Extracted/DWT-SVD-Mode1_"+image_path[49:]

        if not image_path:
            image_path = self.path_save
        img = cv2.imread(image_path,0)
        img = cv2.resize(img, self.shape_watermark)
        img_components = Components()
        img_components.Coefficients, img_components.U, img_components.S, img_components.V = self.calculate(img)
        ratio_ = self.ratio if not ratio else ratio
        self.S_W = (img_components.S - self.img_components.S) / ratio_
        watermark_extracted = self.recover("W")
        cv2.imwrite(extracted_watermark_path, watermark_extracted)

    def embed(self):
        self.S_img = self.img_components.S + self.ratio * self.W_components.S * \
                                             (self.img_components.S.max() / self.W_components.S.max())


def resize(path, watermark):
    dim = (512, 512)

    newPath="./Watermark/512-"+watermark[12:]

    watermark_image = cv2.imread(watermark)
    watermark_image = cv2.resize(watermark_image, dim)
    watermark_image = cv2.imwrite(newPath, watermark_image)


    newPath = "./resizedImages/" + path[9:]

    img = cv2.imread(path)
    img = cv2.resize(img, dim)
    img = cv2.imwrite(newPath, img)


def launch(path, watermark):
    resize(path, watermark)
    print("Running on "+path[9:])
    watermarked="./DWT_SVD_resultsMode1/Watermarked/DWT-SVD-Mode1_"+path[9:]

    watermark_class=watermarking(watermark_path="./Watermark/512-"+watermark[12:])

    watermark_class.watermark(img="./resizedImages/"+path[9:], path_save=None)
    watermark_class.extracted(image_path=watermarked, extracted_watermark_path=None)

