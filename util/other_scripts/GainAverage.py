import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_context('poster')
sns.set(font_scale=1.4)

with open("../../DB/Gains2022/combined_new_gains.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["EXP2SPE"])
dat["EXP2SPE"].keys()

#with open("../../DB/teals_finalV_gains/combined_finalV_gains.json","r") as f:
with open("../../DB/gains_database.json","r") as f:
    dat = json.load(f)
pdf1 = pd.DataFrame(dat["EXP2SPE"])
print(dat["EXP2SPE"].keys())

fig1, ax1 = plt.subplots()
TUBES = np.arange(332,464,1)
count = 0
myy = 0.0
for cnum in TUBES:
	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
            print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
            continue
	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
        	print(cnum)	
        	count = count +1 
        	myy += pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
        	#myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
        	#myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
print(count)
print(myy)
print("the average of the gains is %f" %(myy/count))
