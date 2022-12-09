import matplotlib.pyplot as plt
import numpy as np
def cum_historgram(image):
    n,m = image.shape
    histo = np.zeros(256) # number of gray levels
    for i  in range(n):
        for j in range(m):
            pos = image[i,j]
            histo[pos]+=1
    histo_cum=histo/(n*m)
    for k in range(1,256):
        histo_cum[k]+=histo_cum[k-1]
    return histo,histo_cum

def mean_level(h,n,m,lev):
    histo=h.copy()
    histo/=m*n
    mean=0
    for i in range(lev):
        mean+=i*histo[i]
    return mean

def otsu(image):
    n,m = image.shape
    histo,cum_h = cum_historgram(image)[0], cum_historgram(image)[1]
    mean = mean_level(histo,n,m,256)
    
    var_max,t_max=0,0
    for t in range(1,256):
        wt = cum_h[t-1]
        mean_t=mean_level(histo,n,m,t)
            
        if (wt>0) and (wt<1):
            var_t = ((mean*wt-mean_t)**2)/(wt*(1-wt)) 
            if var_t>var_max:
                var_max=var_t
                t_max = t
    return t_max