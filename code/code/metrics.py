import numpy as np
from sklearn.metrics import jaccard_score

def lesion_pixels(image1,image2):
    """ This function calculates TP, TN, FP and FN and having as input two segmented images."""

    #TP :shows the number of pixels which are classified as lesion in both manual and automatic segmented images.
    #TN : represents the number of pixels which are classified as surrounding normal skin in both manual and automatic borders.
    #FP : indicates the number of pixels which are classified as lesion in automatic segmentation but are labelled as normal skin in manual segmentation.
    #FN : shows the number of pixels which are classified as normal skin in the automatic border but are labelled as lesion in the ground truth image. 

    M1,M2 = image1.copy(),image2.copy()
    n1,m1 = M1.shape
    n2,m2 = M2.shape
     
    TP,TN,FP,FN = 0,0,0,0
    for i in range(n1):
        for j in range(m1):
            if (M1[i,j]==1)and (M2[i,j]==1):
                TP+=1
            elif (M1[i,j]==1)and (M2[i,j]==0):
                FP+=1
            elif (M1[i,j]==0)and (M2[i,j]==1):
                FN+=1
            elif (M1[i,j]==0)and (M2[i,j]==0):
                TN+=1
    return TP,TN,FP,FN

def statistics(image1,image2):
    
    """ This function calculates the four metrics sensitivity, specificity,accuracy
    and similarity (which is used as the Dice metric) using specific formulars 
    that use the values of TP,TN,FP,FN determined by the function lesion_pixels.
    These metrics allows to compare the two input segmented images : image 1 is
    automated image and image 2 is the manual image."""

    manual_image=image2.copy()
    automated_image=image1.copy()
    TP,TN,FP,FN = lesion_pixels(automated_image,manual_image)
    sensitivity = TP /(TP+FN)
    specificity = TN /(TN+FP)
    accuracy = (TP+TN)/(TP+TN+FP+FN)
    similarity = (2*TP)/(2*TP +FN+FP)
    return sensitivity,specificity,accuracy,similarity


def Jaccard_Index (image1,image2):
    
    """ This function calculates the jaccard index which is defined as the 
    cardinal of the intersection between the two images( the segmented image 
    and the ground truth) divided by the cardinality of their unions """
    
    # Tha variables: 
    
        # image1_ : the linear vector constrcted from the original image 
        # image2_ : the linear vector constructed from the ground truth
    
    image1_ = np.ravel(image1)
    image2_ = np.ravel(image2)
    
    return(jaccard_score(image1_,image2_))
