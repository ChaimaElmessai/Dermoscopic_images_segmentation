import numpy as np
import cv2,os
from otsu import otsu
import pillbox
from intensity_adju import Intensity_Adjustement
from CCA import * 
from channel_transform import color_channel
from dilation import fill_holes
import border

def segment(image):

    """ This function perfomrs the whole segmentation process starting by the preprocessing, the the thresholding and finally post processing."""
    original_image=image.copy()
    
    
    # Filtering 
    
    filtered_image = pillbox.Circular_Filter(original_image,5)
    
    #Intensity adjustement
    
    adjusted_image=Intensity_Adjustement(filtered_image,1,99)
    
    # Thresholding
    
    adjusted_image_gray = np.rint(adjusted_image*255).astype(int)
    t = otsu(adjusted_image_gray)
    n,m = adjusted_image_gray.shape
    th_image = np.zeros((n,m)) # the result of Threshold.
    for i  in range(n):
        for j in range(m):
            if adjusted_image_gray[i,j]>t:
                th_image[i,j]=1
                
    # CCA 
    image0=th_image.copy()
    image0 = 1-image0
    
    # Generating runs 
    d = runs(image0)

    # Genrating label equivalences and updating the runs dictionary
    equi,tuples = equivalence(image0,d)

    # Generating connected label equivalences
    conn_tuples = connected_tuples(tuples)
    
    # New Labeling of the runs dictionary.
    for i in range(len(equi)):
        labeling(conn_tuples,equi[i]) 
    
    # Counting the number of pixels of each class (runs belonging to the same class (area) are those having the same label)
    labels ={}
    for k in equi.keys():
        for r in equi[k]:
            if r[0] in labels.keys():
                labels[r[0]]+=r[2]-r[1]+1
            else:
                labels[r[0]]=r[2]-r[1]+1
                
    # Finding the biggest area of the image.
    max1,max2 = min_max_pixels(labels)
    image=image0.copy()
   
    # Interpolating the result of otsu image by turning off(assining 0) pixels that don't belong to the biggest area of the image. 
    for k in equi.keys():
            for r in equi[k]:
                if r[0] != max1:
                    image[k,r[1]:r[2]+1]=np.zeros((1,r[2]-r[1]+1))
    cca_image = (1-image).copy()

    
    # Morphological
    
    dilated = fill_holes(image,12)
    
    return [filtered_image,adjusted_image,th_image,cca_image,dilated]