import numpy as np
def runs(im):
 
    """ This function  operates the first scan of the image to finally return 
       the dictionnary containing the key and the value of the following form : {n°ligne : (Label,start,end)}
       where label : n° of run in the image , start : n° of starting pixel of the run , end : n° of pixel wehre the run ends.
    """
        

    # The variables : 

        # Dic: The dictionnary of runs for each row of the image .
        # label : N° of runs.
        # R : i-th row of the image.
  
    image = im.copy()
    n,m = image.shape
    dic = {}
    label = 0
    for i in range(n):
        dic[i]=[]
        R = image[i]
        j,k =0,0
        while j<m:
            p = R[j]
            if p == 1 :
                label+=1
                k = j+1
                t = (j,j)
                while k<m:
                    if R[k]==0:
                        break
                    k+=1
                dic[i].append([label,j,k-1])
                j=k+1
            else:
                j+=1
    return dic   
def equivalence(im,d):

    """ This function  operates the second scan of the image to finally return the updated dictionary where labels and label equivalences are notes. 
      This second scan starts from the runs in the second row and is operated between the adjacent rows."""
    # The variables : 

        # Dic: The dictionnary of runs for each row of the image .
        # tuples : Variable to store All tuples representing label equivalences .
        # R1,R2 : runs extracted from the dictionary of respectively (i-1)-th and i-th row of the image .


    image = im.copy()
    dic = d.copy()
    n,m = image.shape
    tuples=[]
    for i in range(1,n):
        R1,R2 = dic[i-1],dic[i]
        if R1!=[]:
            for j in range(len(R2)):
                
                # Updating the label of connected runs , once the first run k is found and verfies the condition of connection the scan is sstoped.
                for k in range(len(R1)):
                    if (R1[k][2]>=R2[j][1]-1)&(R1[k][1]<=R2[j][2]+1):
                        R2[j][0]=R1[k][0]
                        break

                # Creating label equivalences 
                if len(R1)!=1:
                    for h in range(k+1,len(R1)):
                        if (R1[h][2]>=R2[j][1]-1)&(R1[h][1]<=R2[j][2]+1):
                            R1[h][0]=(R2[j][0],R1[h][0]) 
                            tuples.append(R1[h][0])   
        dic[i-1],dic[i]=R1,R2
    return  dic,tuples    

def connected_tuples(pairs):

    """ This function operated the search of connected tuples and returns the set of of tuples of connected label equivalences.
        An example :For pairs=[(1, 2), (2, 4), (7, 2) ,(1, 5) ,(6, 3), (8, 3)] the output is {(1, 2, 4, 7, 5), (6, 3, 8)}."""
    # The variables : 

        # Pairs: List of all tuples representing label equivalences.
        # make_new_list_for :
        # add_element_to_list :
        # merge_lists :
     
    # for every element, we keep a reference to the list it belongs to
    lists_by_element = {}

    def make_new_list_for(x, y):
        lists_by_element[x] = lists_by_element[y] = [x, y]

    def add_element_to_list(lst, el):
        lst.append(el)
        lists_by_element[el] = lst

    def merge_lists(lst1, lst2):
        merged_list = lst1 + lst2
        for el in merged_list:
            lists_by_element[el] = merged_list

    for x, y in pairs:
        xList = lists_by_element.get(x)
        yList = lists_by_element.get(y)

        if not xList and not yList:
            make_new_list_for(x, y)

        if xList and not yList:
            add_element_to_list(xList, y)

        if yList and not xList:
            add_element_to_list(yList, x)            

        if xList and yList and xList != yList:
            merge_lists(xList, yList)

    # return the unique lists present in the dictionary
    return set(tuple(l) for l in lists_by_element.values())

def labeling(con_tuples,h):

    """ This procedure operates on a given row of the dictionary to modify provisional label.
      It assigns the smallest label for all connected runs labled by a simple label or a label equivalence."""
    # The variables : 

        # h: i-th value of the dictionary containing all runs encoding.
        # con_tuples : The set of connected label equivalences : Output of the previous function .
      
    t = con_tuples.copy()
    #h = equiv.copy()
    for i in range(len(h)):
        for tuple_ in t:
            #assigning the smallest label for all connected runs labled by a simple label.
            if isinstance(h[i][0],int):
                if h[i][0] in tuple_:
                    h[i][0]=tuple_[0]
                    break
            #assigning the smallest label for all connected runs labled by label equivalence.
            elif h[i][0][0] in tuple_ or h[i][0][1] in tuple_:
                h[i][0]=tuple_[0]
                
def min_max_pixels(dic):

    """ This function returns lables of biggest and the second biggest area of the image."""
    # The variables : 

        # dic: dictionnary of all classes and the number of pixels of each class. 
        # k1,k2 : lables of biggest and the second biggest area of the image.
        # max1,max2 : number of pixels in the biggest and the second biggest area of the image.

    max1,max2=0,0
    k1,k2=0,0
    for (k,v) in dic.items():
        if v>max1:
            max2,k2=max1,k1
            max1,k1=v,k
        elif v >max2:
            max2,k2=v,k
    return(k1,k2)