import matplotlib.pyplot as plt
import numpy as np
import json

dictionary = json.load( open("combined_goodpmts.json","r"))
xAxis = dictionary["EXP2SPE"]["c1Mu"]

dictionary = json.load( open("combined_badpmtsrecovered.json","r"))
xAxisbad = dictionary["SimpleGauss"]["c1Mu"]

print("xAxis :"+ str(xAxis))
#print("yAxis :"+ str(yAxis))
#plt.grid(True)

## LINE GRAPH ##
#plt.plot(xAxis,yAxis, color='maroon', marker='o')
#plt.xlabel('variable')
#plt.ylabel('value')
#plt.show()
#
v=np.array(xAxis)
y=np.array(xAxisbad)
print('xAxis')
print(xAxis)
print('xAxisbad')
print(xAxisbad)
x=np.concatenate((v,y),axis=0)
print('x')
print(x)

z=x*(10**(-9))/(1.6*(10**(-19)))
print("Gains :"+ str(z))
plt.hist(z, density=False, bins=30, range =(0.13E7,1.04E7))
#plt.hist(z, density=False )
plt.xlabel("PMT Gain",fontsize =25)
plt.ylabel("Number of PMTs",fontsize=25)
plt.yticks(fontsize=18)
plt.xticks(fontsize=18)
#plt.rcParams['xtick.labelsize']=18
#plt.rcParams['ytick.labelsize']=18
plt.grid()
plt.show()


## BAR GRAPH ##
#fig = plt.figure()
#plt.bar(xAxis,yAxis, color='maroon')
#plt.xlabel('variable')
#plt.ylabel('value')
#
#plt.show()
