from skimage.morphology import dilation
from skimage.morphology import disk 
import numpy as np
def fill_holes(im,r):


   
  """ This function allows to perform the morphological dilation of the 
        input image with a circular structuring element of size r which is
        the second input of the function .So it allows to fill the holes
        that might be present in the binary image and returns a filled image"""
        

    # The variables : 

        # L: defining the size of the two-dimensional “meshgrid”.
        # x,y : Two-dimensional “meshgrid”.
        # mask : the mask of the structuring element.
        # dilated_image: the filled image. 


  image = im.copy()
  L = np.arange(-r, r + 1)
  x,y= np.meshgrid(L, L)
  mask= x**2+y**2 <= r**2
  mask = mask.astype(np.float32)
  dilated = dilation(image, mask)
  return dilated