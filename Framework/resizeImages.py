
from PIL import Image
import os, sys

path = "C:\\Users\\matte\\PycharmProjects\\DataCompression\\Images\\"
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((32,32), Image.ANTIALIAS)
            imResize.save(f + ' resized.bmp', quality=90)

resize()