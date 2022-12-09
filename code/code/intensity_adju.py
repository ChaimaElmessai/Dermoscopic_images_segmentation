# Import libraries
import numpy as np
from skimage import exposure
import matplotlib.pyplot as plt
import cv2

 

def Intensity_Adjustement(im, p1, p2) :
  """ This function allows to stretch the histogram of the input image by 
  scaling the intensity values such that 1% of the data is satured at 0 (the lowest value) 
  and 1(the highest value) because in our case p1=1 et p2=99"""
        
    # The variables : 

        # p1,p99 : Two percentiles: the dynamic range of pixel values of the image 
                   #is mapped into a range which is defined by these two percentiles.
                        
        # stretched_image : the stretched image. 
    
  per1, per2 = np.percentile(im, (p1, p2))
  img_stretched = exposure.rescale_intensity(im, in_range = (per1, per2))

  return img_stretched