import numpy as np
from skimage import color
def color_channel(image,space='RGB'):
    
    """ This function allows to generate a dictionary  whose keys are the names 
    of the channels and the values are the channeled images (the input RGB
    image in the corresponding channels of the key).These channels are 10         
    channels determined from different color spaces : RGB, LAB, YCbCr and 
    XYZ colors spaces."""

    channels = {}
    im = image.copy()
    im=im.astype(np.int)
    n,m = im.shape[0],im.shape[1]

    #channels determined from RGB color space which are : R,G,B,RGB and I channels.

    R,G,B = im[:,:,0],im[:,:,1],im[:,:,2]
    channels['R'],channels['G'],channels['B'] = R,G,B
    channels['RGB'] = 0.299*R + 0.587*G + 0.114*B
    channels['I'] = (R+G+B)/3
    #channels['S'] = 1-(3*np.minimum(np.minimum(R,G),B))/(R+G+B)
    
    H = np.zeros((n,m))
    for i in range(n):
        for j in range(m):
            R_,G_,B_=R[i,j],G[i,j],B[i,j]
            W = np.arccos((R_-G_/2-B_/2)/np.sqrt((R_-G_)**2+(R_-B_)*(G_-B_)))
            if G_>B_:
                H[i,j]=W
            else:
                H[i,j]=2*np.pi - W
    #channels['H'] = H
    
    
     # The channel L determined from LAB color space.
 
    im_lab = color.rgb2lab(im)
    channels['L'] = im_lab[:,:,0]
    
    # The Channel YCbCr of YCbCr color space determined using the matrix T1.
    
    T1 = np.array([[.299, .587, .114], [-.1687, -.3313, .5], [.5, -.4187, -.0813]])
    YCbCr = im.dot(T1.T)
    YCbCr[:,:,[1,2]] += 128
    channels['YCbCr'] = YCbCr[:,:,0]


     # Channels of  X,Y,Z color space determined from the R,G and B values using this matrix : 
     # [[0.4125, 0.3576, 0.1804],
     #  [0.2127, 0.7152, 0.0722],
     #   [0.0193, 0.119, 0.9502]]
    
    
    X = 0.4125*R+ 0.3576*G+ 0.1804*B
    Y = 0.2127*R+ 0.7152*G+ 0.0722*B
    Z = 0.0193*R+ 0.119*G+ 0.9502*B
    channels['X'],channels['Y'],channels['Z'] = X,Y,Z
    return channels