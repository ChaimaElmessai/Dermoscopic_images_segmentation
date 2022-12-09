import numpy as np

def mask(G,T):
    """ This function  return the binary mask obtained by thresholding the grayscale image."""
    # The variables : 

        # G:the grayscale image  .
        # T : threshold.
    M = np.zeros(G.shape)
    for x in range(G.shape[0]) :
        for y in range(G.shape[1]):
            if G[x,y] > T:
                M[x,y] = 1 
    return M

def hair_mask(Mr,Mg,Mb):

    """ This function  returns the final binary mask obtained by computing the Union of three Mj masks for each RGB channel."""
    # The variables : 

        # G:the grayscale image  .
        # T : threshold.
    mr,mg,mb = Mr.reshape(1,-1),Mg.reshape(1,-1) ,Mb.reshape(1,-1) 
    m = np.zeros(mr.shape,dtype='uint8')
    for i  in range(mr.shape[1]):
        if (mr[0,i]==1) or (mg[0,i] == 1) or (mb[0,i] == 1):
            m[0,i]=1
    return m.reshape(Mr.shape)

def lines(x,y,M):
    """ This Function is in charge of calculating the length of eight segments in all directions up,down,left,
    right, and the four diagonals : diag_down,diag_Up,diag_left_down,diag_Right_Up. 
    The output of this function is a dictionnary containing the length of 4 straight lines devided into two segments."""

     # The variables : 

            # c_up (and other variables noted in this way) : are counter variables to calculate the number of pixels == > length of segments

    p = M[x,y]
    s1,s2 = M.shape
    
    i,j = x,y
    
    # Calculating each line segment length
    
    #UP
    c_up ,p1 = 0,p.copy()
    if (p == 0) and (i > 0) :
        c_up +=1
        while i-c_up>=0 :
            p1 = M[i-c_up,j]
            if p1 == 1 :
                c_up -=1
                break
            c_up +=1
        if p1 != 1 :
            c_up -=1
    #Down
    c_down ,p1= 0,p.copy()
    if (p1 == 0) and (i < s1) :
        c_down +=1
        while i+c_down<s1 :
            p1 = M[i+c_down,j]
            if p1 == 1 :
                
                c_down -=1
                break
            c_down +=1
        if p1 != 1 :
            c_down-=1
            
    
    #Left
    c_left ,p1 = 0,p.copy()
    if (p == 0) and (j > 0) :
        c_left +=1
        while j-c_left>=0 :
            p1 = M[i,j-c_left]
            if p1 == 1 :
                c_left -=1
                break
            c_left +=1
        if p1 != 1 :
            c_left -=1
    
    #Right
    c_right ,p1= 0,p.copy()
    if (p == 0) and (j < s2) :
        c_right +=1
        while j+c_right<s2 :
            p1 = M[i,j+c_right]
            if p1 == 1 :
                c_right -=1
                break
            c_right +=1
        if p1 != 1 :
            c_right-=1
            
    
    # Diagonal Down
    
    c_d1 ,p1= 0,p.copy()
    if (p == 0) and (j < s2) and (i < s1):
        c_d1 +=1
        while (j+c_d1<s2) and (i+c_d1<s1) :
            p1 = M[i+c_d1,j+c_d1]
            if p1 == 1 :
                c_d1 -=1
                break
            c_d1 +=1
        if p1 != 1 :
            c_d1-=1
    c_diag_down = c_d1      
            
    # Diagonal Up
    
    c_d2 ,p1= 0,p.copy()
    if (p == 0) and (j > 0) and (i > 0):
        c_d2 +=1
        while (j-c_d2>=0) and (i-c_d2>=0) :
            p1 = M[i-c_d2,j-c_d2]
            if p1 == 1 :
                c_d2 -=1
                break
            c_d2 +=1
        if p1 != 1 :
            c_d2-=1
    
    c_diag_Up = c_d2
    # Diagonal left Down
    
    c_d3 ,p1= 0,p.copy()
    if (p == 0) and (j > 0) and (i < s1):
        c_d3 +=1
        while (j-c_d3>=0) and (i+c_d3<s1) :
            p1 = M[i+c_d3,j-c_d3]
            if p1 == 1 :
                c_d3 -=1
                break
            c_d3 +=1
        if p1 != 1 :
            c_d3-=1
    c_diag_left_down = c_d3    
    # Diagonal Right Up
    
    c_d4 ,p1= 0,p.copy()
    if (p == 0) and (j < s2) and (i > 0):
        c_d4 +=1
        while (j+c_d4 <s2) and (i-c_d4>=0) :
            p1 = M[i-c_d4,j+c_d4]
            if p1 == 1 :
                c_d4 -=1
                break
            c_d4 +=1
        if p1 != 1 :
            c_d4-=1
    
    c_diag_Right_Up = c_d4 
    
    # Calculating the 4 lines length
    
    line1 = c_up + c_down
    line2 = c_left + c_right
    line3 = c_diag_down + c_diag_Up
    line4 = c_diag_left_down + c_diag_Right_Up
    
    d_lines = {}
    d_lines['Vertical'] = (c_up , c_down)
    d_lines['Horizontal'] = (c_left , c_right)
    d_lines['Diag1'] = (c_diag_Up , c_diag_down )
    d_lines['Diag2'] = (c_diag_Right_Up,c_diag_left_down)
    return d_lines
    
# t1 nd t2 are the respectively the high and low threshold
def locate(Mask,t1,t2):

    """This function is charged of browsing the input mask, calculating lines of each pixel and decides wether
    the pixel of concern is rejected or kept inside the hair structure. The criteria of this process is as follows :
    
    * t1 and t2 : two thersholds given as input .
    * The longest line must be longer than t1 pixels and other lines must be shorter than 10 pixels.  """
    
    M = Mask.copy()
    s1,s2 = M.shape
    for x  in range(s1):        
        for y in range(s2):
            # generating the 4 lines for each pixel.
            d = lines(x,y,M)
            l1,l2,l3,l4 = d['Vertical'],d['Horizontal'],d['Diag1'],d['Diag2']
            l_max = max(sum(l1),sum(l2),sum(l3),sum(l4))
            l_min = min(sum(l1),sum(l2),sum(l3),sum(l4))
            if (l_max < t1) or (l_min > t2):
                M[x,y] = 1
            
    return M

def bilinear(im,i,j,seg1,seg2,direction,mask,s):

    """This function outputs positions of the two non hair pixels that will be used in the interpolation step."""

     # The variables : 

          # Direction : The direction on wich we will operate the inerpolation.
          # seg1,seg2 : Length of two segments forming the considered line (of minimal line).
          # i,j : Position of the hair pixel which will be replaced by interpolation.
          # s : The number of pixel from which we interpolate. It represents the distance between the hair determined hair edge (seg1,seg2) 
          #     and pixels used in interpolation process.

    s1,s2=im.shape    
    if direction=='Vertical':
        up,down = seg1,seg2 
        x1,y1,x2,y2 = i-(up+s),j,i+(up+s),j
        if x1<0 : x1=0
        if x2>=s1 : x2=s1-1
        return x1,y1,x2,y2
    elif direction=='Horizontal':
        left,right = seg1,seg2
        x1,y1,x2,y2 = i,j-(left+s),i,j+(right+s)
        if y1<0 : y1=0
        if y2>=s2 : y2=s2-1
        return  x1,y1,x2,y2
    elif direction=='Diag1':
        diag_up,diag_down = seg1,seg2
        x1,y1,x2,y2 = i-(diag_up+s),j-(diag_up+s),i+(diag_down+s),j+(diag_down+s)
        if x1<0 : x1=0
        if x2>=s1 : x2=s1-1
        if y1<0 : y1=0
        if y2>=s2 : y2=s1-1
        return  x1,y1,x2,y2  
    else:
        diag_right_up,diag_left_down = seg1,seg2
        x1,y1,x2,y2 =i-(diag_right_up+s),j+(diag_right_up+s),i+(diag_left_down+s),j-(diag_left_down+s)
        if x1<0 : x1=0
        if x2>=s1 : x2=s1-1
        if y2<0 : y2=0
        if y1>=s2 : y1=s1-1
        return  x1,y1,x2,y2 
    
def distance(a,b,c,d):
    """calculates the ddistance between two pixels"""
    return np.sqrt((c-a)**2 + (d-b)**2)

# 

def interpolate(M,image,s):
    """Interpolate  : return the interpolated matrix"""
    # The variables :
      
       # s : Has the same role as in the previous function.

    im = image.copy()
    s1,s2 = M.shape
    
    # Browse all pixels
    for x  in range(s1):  
        for y in range(s2):
            if M[x,y] == 0 :

                # generating the 4 lines for each hair pixel.
                d = lines(x,y,M) 
                directions =['Vertical','Horizontal','Diag1','Diag2'] 
                lines_= d['Vertical'],d['Horizontal'],d['Diag1'],d['Diag2']

                # Finding the line with the minimum length.
                lmin = sum(lines_[0])
                ind_min = 0
                for i in range(1,4):
                    if sum(lines_[i])<lmin : 
                        lmin = sum(lines_[i])
                        ind_min = i

                # Generting segmements of the found line.
                seg_min1,seg_min2= lines_[ind_min]
                direction = directions[ind_min]

                # Finding the position of non hair pixels that will be used in the interpolation process.
                x1,y1,x2,y2 = bilinear(im,x,y,seg_min1,seg_min2,direction,M,s)
                I1= im[x1,y1] # Intensity of first pixel 
                I2 = im[x2,y2]  # Intensity of the second pixel 
                
                # Calculating the distance between the considered pixels
                d = distance(x1,y1,x2,y2) # between non hair pixels
                d1 = distance(x,y,x1,y1)  # between hair pixel and first non hair pixels
                d2 = distance(x,y,x2,y2)  # between hair pixel and second non hair pixels
                In =I2*(d1/d) + I1*(d2/d) # bilinear inteprolation.
                im[x,y] = In
            
    return im