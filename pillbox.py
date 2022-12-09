from scipy import signal
import numpy as np

"""This function allows to smooth the input image using a circular averaging 
    low-pass filter with radius r which is the second input of the function.This 
    filter is used to remove the artifacts that might be present in the image.""" 

    
    # The variables : 

        # y,x : Two-dimensional “meshgrid”.
        
        # mask : the mask of the filter:It contains boolean values.So by constructing
                 #the variable kernel and using the instruction kernel[mask]=1,we convert 
                 # the boolean values to float values that are stocked in kernel.
                
        # smoothed_image : the filtered image. 

def Circular_Filter(im,r):
    image=im.copy()
    kernel=np.zeros((2*r+1,2*r+1))
    y,x = np.ogrid[-r: r+1, -r: r+1]
    mask= x**2+y**2 <= r**2#  la définition 
    kernel[mask]=1
    smoothed_image =signal.convolve2d(image, kernel,mode='same', boundary='fill', fillvalue=0)
    return smoothed_image