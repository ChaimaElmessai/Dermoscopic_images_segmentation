import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys
from  PIL  import Image

def New_method(img):
    
    """This function allows to obtain an image without the black frame proceeding in four steps which are 
        1- converting the image to gray
        2- Detecting the edges using canny filter
        3- thresholding, cerating the mask and applying morphology closure to clean up any extraneous spotand creating the mask
        4- doing bitwise_and to crop the black frame. """
    
    #converting the image to gray
    original = img.copy()
    ed = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    
    #Detecting the edges using canny filter
    
    edges = cv.GaussianBlur(img, (21, 51), 3)
    edges = cv.cvtColor(edges, cv.COLOR_BGR2GRAY)
    edges = cv.Canny(edges, 23, 23)
    
    #thresholding, cerating the mask and applying morphology closure to clean up any extraneous spotand creating the mask
    _, thresh = cv.threshold(edges, 0, 255, cv.THRESH_BINARY  + cv.THRESH_OTSU)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
    mask = cv.morphologyEx(thresh, cv.MORPH_CLOSE, kernel, iterations=4)
    data = mask.tolist()

    for i in  range(len(data)):
        for j in  range(len(data[i])):
            if data[i][j] !=  255:
                data[i][j] =  -1
            else:
                break
        for j in  range(len(data[i])-1, -1, -1):
            if data[i][j] !=  255:
                data[i][j] =  -1
            else:
                break
    image = np.array(data)
    image[image !=  -1] =  255
    image[image ==  -1] =  0
    mask = np.array(image, np.uint8)
    
    # doing bitwise_and to crop the black frame.
    
    result = cv.bitwise_and(original, original, mask=mask)
    result[mask ==  0] =  255
    cv.imwrite('bg.png', result)
    img = Image.open('bg.png')
    img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] ==  255  and item[1] ==  255  and item[2] ==  255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save("img.png", "PNG")
    dest=cv.imread("img.png")
    b, g, r = cv.split(dest)
    dest = cv.merge([r, g, b])
    
    return dest
    

