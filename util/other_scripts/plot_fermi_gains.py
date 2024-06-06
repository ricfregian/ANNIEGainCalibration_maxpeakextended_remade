import matplotlib.pyplot as plt
import numpy as np
import json

#dictionary = json.load(open('../../../gains_json_files/Gains2022_fromhighmean/gains2022.json', 'r'))
#dictionary = json.load(open('../../../gains_json_files/Gains2022_fromlowmean/gains2022.json', 'r'))
#dictionary = json.load(open('../../../gains_json_files/teals_fromlowmean/teals_combined_fromlowmean.json', 'r'))
#dictionary = json.load(open('../../../gains_json_files/gains_database.json', 'r'))
#dictionary = json.load(open('../../../gains_json_files/tealsV3_fromlowmean/tealsV3_combined_fromlowmean.json', 'r'))
#dictionary = json.load(open('../../../gains_json_files/tealsV3_meanp0015.json', 'r'))
#dictionary = json.load(open('../../../gains_json_files/tealsV3_meanp0018.json', 'r'))
#dictionary = json.load(open('../../../gains_json_files/teals_finalV_p0015_tau4s.json', 'r'))
dictionary = json.load(open('../../../gains_json_files/gains2022_fermifit.json', 'r'))

#xAxis = [key for key, value in dictionary["Gauss2"].items()]
xAxis = dictionary["FERMIFIT"]["c1Mu"]
#xAxis = dictionary["c1Mu"]
#xAxis = dictionary["EXP2SPE"]
print("xAxis :"+ str(xAxis))
#print("yAxis :"+ str(yAxis))
#plt.grid(True)

## LINE GRAPH ##
#plt.plot(xAxis,yAxis, color='maroon', marker='o')
#plt.xlabel('variable')
#plt.ylabel('value')
#plt.show()
#
x=np.array(xAxis)
z=x*(10**(-9))/(1.6*(10**(-19)))
print("Gains :"+ str(z))
plt.hist(z, density=False, bins=10, range =(0.13E7,1.04E7))
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
