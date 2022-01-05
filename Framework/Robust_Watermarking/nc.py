import argparse
import cv2
import numpy as np


#La robustezza del watermark è generalmente misurata dal valore della Correlazione Normalizzata (NC).
'''
NC è un numero positivo non maggiore di 1, maggiore è il
valore, migliore è la robustezza dell'algoritmo, ovvero il
watermark estratto. Il più simile al watermark originale; nel caso ideale è 1.

'''





from skimage import io, feature
from scipy import ndimage
import numpy as np

def correlation_coefficient(img1, img2):
    patch1 = cv2.imread(img1)
    patch2 = cv2.imread(img1)

    product = np.mean((patch1 - patch1.mean()) * (patch2 - patch2.mean()))
    stds = patch1.std() * patch2.std()
    if stds == 0:
        return 0
    else:
        product /= stds
        return product

im = io.imread('watermark.png')

im1 = im[16:263, 4:146]
sh_row, sh_col = im1.shape
im2 = im[16:263, 155:155+sh_col]

# Registration of the two images
translation = feature.register_translation(im1, im2, upsample_factor=10)[0]
im2_register = ndimage.shift(im2, translation)

d = 1

correlation = np.zeros_like(im1)

for i in range(d, sh_row - (d + 1)):
    for j in range(d, sh_col - (d + 1)):
        correlation[i, j] = correlation_coefficient(im1[i - d: i + d + 1,
                                                        j - d: j + d + 1],
                                                    im2[i - d: i + d + 1,
                                                        j - d: j + d + 1])

io.imshow(correlation, cmap='gray')
io.show()

correlation_coefficient("watermark.png", "DWT-SVD-Mode1_cameraman.jpeg")