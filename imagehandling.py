from PIL import Image
import numpy as np
import sys

image = Image.open("keycropped.png")
array = np.asarray(image)
array = array.view([(f'f{i}',array.dtype) for i in range(array.shape[-1])])[...,0].astype('O')
unique = list(np.unique(array[:,2]))
unique = [a[0:3] for a in unique]
heights = [0, 1, 2, 6, 13, 25, 44, 70, 105, 151, 209, 279, 356, 466, 585, 724, 882, 1063, 1267, 1495, 1751, 2034]
colordict = dict(zip(unique,heights))
victoria = Image.open("victoria-min.jpg")
vicarray = np.asarray(victoria)
vicarray = vicarray.view([(f'f{i}',vicarray.dtype) for i in range(vicarray.shape[-1])])[...,0].astype('O')
count = np.count_nonzero(np.vectorize(lambda x: x in unique)(vicarray))
def minimize_color_dist(color1, list_of_colors):
    minimum = 255**2
    min_color = None
    for index, color in enumerate(list_of_colors):
        sum = 0
        for i,j in zip(color1, color):
            sum += (i-j)**2
        if sum < minimum:
            minimum = sum
            min_color = color

    return colordict[min_color]

elevation_array = np.vectorize(minimize_color_dist, excluded=["list_of_colors"])(vicarray, list_of_colors=unique)
# print(elevation_array.shape)
# rev_colordict = {item:list(key) for key, item in colordict.items()}
# new_img_array = np.array([[rev_colordict[j] for j in i] for i in elevation_array])
# j = Image.fromarray(np.uint8(new_img_array), "RGB")
# j.show()
