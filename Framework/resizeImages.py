
from PIL import Image
import os, sys
import cv2

path = "C:\\Users\\matte\\PycharmProjects\\DataCompression\\Images\\"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            Image = cv2.imread(path+item, 1)
            Image = cv2.resize(Image, (512, 512))
            #im = Image.open(path+item)
            #f, e = os.path.splitext(path+item)
            #imResize = im.resize((512,512), Image.ANTIALIAS)

            cv2.imwrite("./originalImages/"+item[:-5]+'.jpeg', Image)

resize()