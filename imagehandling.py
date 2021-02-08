from PIL import Image
import numpy as np
import sys
np.set_printoptions(threshold=sys.maxsize)

image = Image.open("keycropped.png")
# print(image.format)
# print(image.size)
# print(image.mode)
array = np.asarray(image)
array = array.view([(f'f{i}',array.dtype) for i in range(array.shape[-1])])[...,0].astype('O')
# print([(f'f{i}',array.dtype) for i in range(array.shape[-1])])
# print(array.shape)
# print(array[1,1])
# # print(array[:,2])
# print(len(np.unique(array[:,2])))
unique = list(np.unique(array[:,2]))

victoria = Image.open("victoria.png")
vicarray = np.asarray(victoria)
# print(vicarray.shape)
vicarray = vicarray.view([(f'f{i}',vicarray.dtype) for i in range(vicarray.shape[-1])])[...,0].astype('O')

ont = np.count_nonzero(np.vectorize(lambda x: x in unique)(vicarray))
print(vicarray[50,50])
print(unique)
print(ont/vicarray.size)
# np.count_nonzero(array in unique)

# print(array)

# b = array.view([(f'f{i}',array.dtype) for i in range(array.shape[-1])])[...,0].astype('O')
# print(b.shape)
# print(b[1,1])
