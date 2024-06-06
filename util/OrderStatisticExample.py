# coding: utf-8
#*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import scipy as scp
import scipy.optimize as sco
import scipy.stats as sts
import scipy.special as sps
import lib.Functions as fu

def OrderStat(x,A,n,mu,s):
    return (n/s)*fu.gauss1(x,A,mu,s)*((1./2)*((1 + sps.erf((x-mu)/s)))**(n-1))

maxes = []
for i in range(10000):
    maxes.append(np.max(scp.randn(30)))
    
bin_height, bin_edges = np.histogram(maxes,bins=100)
bin_width = bin_edges[1]-bin_edges[0]
bin_edges_t = bin_edges[0:len(bin_edges) -1]
bin_centers = np.array(bin_edges_t) - (bin_width/2)
popt,pcov = sco.curve_fit(fu.gauss1,bin_centers,bin_height,p0=[1000,2,2])
yfit = fu.gauss1(bin_centers,popt[0],popt[1],popt[2])
plt.hist(maxes,bins=100)
plt.plot(bin_centers,yfit)
plt.show()
popt,pcov = sco.curve_fit(OrderStat,bin_centers,bin_height,p0=[300,30,1,2],maxfev=10000)
yfit = OrderStat(bin_centers,popt[0],popt[1],popt[2],popt[3])
plt.hist(maxes,bins=100)
plt.plot(bin_centers,yfit)
plt.show()
