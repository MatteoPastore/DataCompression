import os
import random
from csv import writer
import numpy as np
import cv2

def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

########################## attacks ######################################

def awgn(img, std, seed=123):       #rumore gaussiano
    mean = 0.0  # some constant
    np.random.seed(seed)
    attacked = img + np.random.normal(mean, std, img.shape)
    attacked = np.clip(attacked, 0, 255)
    return attacked

def blur(img, sigma):
    from scipy.ndimage.filters import gaussian_filter
    attacked = gaussian_filter(img, sigma)
    return attacked

def sharpening(img, sigma, alpha=1):
    import scipy
    from scipy.ndimage import gaussian_filter
    import matplotlib.pyplot as plt

    # print(img/255)
    filter_blurred_f = gaussian_filter(img, sigma)

    attacked = img + alpha * (img - filter_blurred_f)
    return attacked

def median(img, kernel_size):
    from scipy.signal import medfilt
    attacked = medfilt(img, kernel_size)
    return attacked


def resizing(img, scale):
  from skimage.transform import rescale
  x, y = img.shape
  attacked = rescale(img, scale)
  attacked = rescale(attacked, 1/scale)
  attacked = attacked[:x, :y]
  return attacked

def jpeg_compression(img, QF):
  cv2.imwrite('tmp.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), QF])
  attacked = cv2.imread('tmp.jpg', 0)
  os.remove('tmp.jpg')
  return attacked

def random_attack(img):
    i = random.randint(1, 6)
    if i == 1:
        attacked = awgn(img, 5.0, 123)
    elif i == 2:
        attacked = blur(img, [3, 2])
    elif i == 3:
        attacked = sharpening(img, 1, 1)
    elif i == 4:
        attacked = median(img, [3, 5])
    elif i == 5:
        attacked = resizing(img, 0.5)
    elif i == 6:
        attacked = jpeg_compression(img, 75)
    return attacked

def random_mark(mark_size):
    fakemark = np.random.uniform(0.0, 1.0, mark_size)
    fakemark = np.uint8(np.rint(fakemark))
    return fakemark
def attack_name(numAttack):
    if numAttack == 0:
        return "awgn"
    elif numAttack == 1:
        return "blur"
    elif numAttack == 2:
        return "sharpening"
    elif numAttack == 3:
        return "median"
    elif numAttack == 4:
        return "resizing"
    elif numAttack == 5:
        return "jpeg"

######################################################################