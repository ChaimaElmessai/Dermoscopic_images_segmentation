def LightnessComponentHSL(image,i,j):

    """ This function calculates the lightness component of the HSL color space of a pixel 
        of the input image.This value will be utilized to determine the darkness of the pixel."""


    L=(max(image[i,j,0], image[i,j,1], image[i,j,2])+min(image[i,j,0], image[i,j,1], image[i,j,2]))/2
    return L

def test(image,n):
    """ This function takes the input image and a variable n which takes two values( 0 if we scroll 
        the rows, 1 if we scroll the columns) and returns the two indices of rows or columns 
        (depending on the value of n) which limit the image without black frame"""
    
    # The variables
        
        # t1: the percentage of black pixels in a row if n=0 and if we scroll from top to bottom 
              #or the percentage of black pixels in a column if n=1 and if we scroll from right to left.
            
        #t2 : the percentage of black pixels in a row if n=0 and if we scroll from bottom to top 
              #or the percentage of black pixels in a column if n=1 and if we scroll from left to right.
        
        # nb1: The number of black pixels in a row if n=0 and we scroll from top to the buttom
               # or the number of black pixels in a column if n=1 and we scroll from right to left. 
        # nb2: The number of black pixels in a row if n=0 and we scroll from bottom to the top
               # or the number of black pixels in a column if n=1 and we scroll from left to right.
        # L: the lightness component of the HSL color space of a pixel.
        # indice1,indice2: The two indexes delimiting the image without black frame 
    if n==0:
        n1=1
    else :
        n1=0
    i=0
    t1=60
    
    while(i<image.shape[n])&(t1>=60):
        np1=0
        t1=0
        for j in range(image.shape[n1]):
            if n==0 :
                L=LightnessComponentHSL(image,i,j)
            else : 
                L=LightnessComponentHSL(image,j,i)
            if (L<20):
                np1=np1+1
        t1=(np1/image.shape[n])*100    
        i=i+1
    indice1=i-1
    
    #parcourir de bas en haut ou de gauche à droite
    k=image.shape[n]-1
    t2=60
    while(k>=0)&(t2>=60):
        np2=0
        t2=0
        for j in range(image.shape[n1]):
            if n==0 :
                L=LightnessComponentHSL(image,k,j)
            else:
                L=LightnessComponentHSL(image,j,k)
            if (L<20):
                np2=np2+1
        t2=(np2/image.shape[n])*100    
        k=k-1
    indice2=k-1
    return(indice1,indice2)