import numpy as np
import math
import argparse
import os
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import copy

rows, cols = (4, 4)

def img2bin(row,col,name):
    convertedImg = np.zeros((row, col))
    #open image (binary image) from https://www.pixilart.com/draw?ref=home-page
    binImg = Image.open(name)
    binImg = np.array(binImg)

    # Convert binary image rgba code [0 0 0 255] or [0 0 0 0] to 1 and -1 (memeory array)
    for r in range(row):
        for c in range(col):
            if binImg[r][c][3] > 0.5:
                convertedImg[r][c] = 1
            else:
                convertedImg[r][c] = -1
    return convertedImg


def pad_zeros_2_list(thisArray,r,c):
    padded_array = np.zeros((r+2,c+2))-1
    padded_array[1:thisArray.shape[0]+1, 1:thisArray.shape[1]+1] = thisArray
    return padded_array


img = img2bin(4,4,'testImg.png')
print(img)

# plt.imshow(img, cmap='Greys')
# plt.show()






