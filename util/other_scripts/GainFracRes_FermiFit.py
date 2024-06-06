# coding: utf-8

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_context('poster')
sns.set(font_scale=1.4)

#with open("../../DB/Gains2022/combined_new_gains.json","r") as f:
with open("../../../gains_json_files/gains_database.json","r") as f:
#with open("../../DB/teals_fromlowmean/teals_combined_fromlowmean.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["EXP2SPE"])
dat["EXP2SPE"].keys()

#with open("../../../gains_json_files/teals_finalV_gains/combined_finalV_gains.json","r") as f:
#with open("../../../gains_json_files/Gains2022/combined_new_gains.json","r") as f:
#with open("../../../gains_json_files/newgains_doublestat_manual.json","r") as f:
#with open("../../../gains_json_files/tealsV3_fromlowmean/tealsV3_combined_fromlowmean.json","r") as f:
#with open("../../../gains_json_files/Gains2022_fromlowmean/gains2022.json","r") as f:
#with open("../../../gains_json_files/teals_fromlowmean/teals_combined_fromlowmean.json","r") as f:
#with open("../../../gains_json_files/GianGains.json","r") as f:
#with open("../../../gains_json_files/teals_finalV_p0015_tau4s.json","r") as f:
#with open("../../../gains_json_files/teals_finalV_p0015_tau4s.json","r") as f:
#with open("../../../gains_json_files/teals_finalV_seed.json","r") as f:
#with open("../../../gains_json_files/teals_V3_seed.json","r") as f:
#with open("../../../gains_json_files/teals_finalV_seed_nowrongfits.json","r") as f:
with open("../../../gains_json_files/gains2022_fermifit.json","r") as f:
#
#    dat = json.load(f)
#pdf1 = pd.DataFrame(dat["EXP2SPE"])
#print(dat["EXP2SPE"].keys())

    dat = json.load(f)
pdf1 = pd.DataFrame(dat["FERMIFIT"])
print(dat["FERMIFIT"].keys())

z=(10**(-9))/(1.6*(10**(-19)))

fig1,ax1 = plt.subplots()

TUBES = np.arange(332,464,1)
for cnum in TUBES:
	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
            print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
            continue
	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
        	print(cnum)
        	myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
        	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
        	#myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
        	ax1.errorbar((myy-myx)/myy,cnum,alpha=0.8,linestyle='None',marker='o',markersize=10)
        	if((myy-myx)< 0):
       		 print("negative residual in channel: %i " %(cnum))
        	if(((myy-myx)/myy)> 0.4):
       		 print(" residual greater than 0.4 in channel: %i " %(cnum))
        	if(((myy-myx)/myy)< 0.1):
       		 print(" residual smaller than 0.1 in channel: %i " %(cnum))

#plt.ylim([0.0,0.0025 ])
plt.legend(loc = "upper right")
plt.xlabel("Fractional residual")
plt.ylabel("Channel")
plt.title("")
plt.rcParams['axes.unicode_minus'] = False #display minus sign in the axis coordinates
plt.show()


frac_res_temp = []
fig2,ax2 = plt.subplots()

TUBES = np.arange(332,464,1)
for cnum in TUBES:
	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
            print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
            continue
	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
        	print(cnum)
        	myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
        	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
        	#myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
       		frac_res_temp.append((myy-myx)/myy)
        	#ax2.hist((myy-myx)/myy,density = False)

frac_res=np.array(frac_res_temp)
#ax2.hist(frac_res,density = False)
ax2.hist(frac_res, density=False, bins=15, range =(-0.8,0.8))
#plt.ylim([0.0,0.0025 ])
plt.legend(loc = "upper right")
plt.xlabel("Fractional residual")
plt.ylabel("Entries")
plt.title("")
plt.rcParams['axes.unicode_minus'] = False #display minus sign in the axis coordinates
plt.show()

