
from PIL import Image
from numpy import asarray

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

filename = 'immagineProva'

img = Image.open( filename + '.bmp' )
data = np.array( img, dtype='uint8' )

np.save( filename + '.npy', data)

# visually testing our output
img_array = np.load(filename + '.npy')
from matplotlib import pyplot as plt

plt.imshow(img_array, cmap='gray')
plt.show()