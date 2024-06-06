# coding: utf-8

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

with open("../../DB/teals_finalV_gains/combined_finalV_gains.json","r") as f:
    dat = json.load(f)
pdf1 = pd.DataFrame(dat["EXP2SPE"])
print(dat["EXP2SPE"].keys())
#for key in dat["EXP2SPE"].keys()
#  if key = 'c1Mu'
#	print "hello"
#


z=(10**(-9))/(1.6*(10**(-19)))
plt.errorbar(x='Channel', y='c1Mu', data=pdf, yerr = 'c1Mu_unc', xerr = None, ls='none', marker = 'o', markersize = 10, alpha = 0.8)
plt.errorbar(x='Channel', y='c1Mu', data=pdf1, yerr = 'c1Mu_unc', xerr = None, ls='none',  marker = 'o',markersize = 10, alpha = 0.8)
plt.xlabel("Channel")
plt.ylabel("SPE Charge mean (nC)")
plt.title("Mean SPE charge fits over 5 days")
plt.show()

sns.pointplot(x='Channel', y='c1Mu', data=pdf, join=False, ci=None, color = "k")
sns.pointplot(x='Channel', y='c1Mu', data=pdf1, join=False)
plt.xlabel("Channel")
plt.ylabel("SPE Charge mean (nC)")
plt.title("Mean SPE charge fits over 5 days")
plt.show()

ax=sns.pointplot(x='Channel', y='c1Mu', data=pdf, join=False, ci=None, color = "k")
#sns.pointplot(x='Channel', y='c1Mu', data=pdf1, join=False)
# Find the x,y coordinates for each point
x_coords = []
y_coords = []
for point_pair in ax.collections:
    for x, y in point_pair.get_offsets():
        x_coords.append(x)
        y_coords.append(y)
#numpy array of the errors 
#this could have been done for the x and y channel also 
error = np.array(list(set(pdf['c1Mu_unc'])))
# Calculate the type of error to plot as the error bars
# Make sure the order is the same as the points were looped over
#errors=pdf.groupby(['Channel']).std()['c1Mu']
ax.errorbar(x_coords, y_coords, yerr=error, fmt=' ',zorder =-1 )
plt.xlabel("Channel")
plt.ylabel("SPE Charge mean (nC)")
plt.title("Mean SPE charge fits over 5 days")
plt.show()

fig_, ax_ = plt.subplots()
TUBES = np.arange(332,464,1)
for cnum in TUBES:
	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
            print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
            continue
	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
        	print(cnum)
        	myx = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
        	myy = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
        	#myy = pdf.loc[(pdf["Channel"] == cnum), "Channel"].values
        	myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
        	ax_.errorbar(myx,myy,alpha=0.8,label="%i Data"%cnum,linestyle='None',marker='o',markersize=6)
plt.axline((0.0, 0.0), slope=1.0, color="black", linestyle=(0, (5, 5)))
plt.xlabel("Channel")
plt.ylabel("SPE Charge mean (nC)")
plt.title("Mean SPE charge fits over 5 days")
plt.show()

sns.barplot(x='Channel', y='c1Mu', estimator=np.mean,data=pdf)
plt.xlabel("Channel")
plt.ylabel("SPE Charge mean (nC)")
plt.title("Mean SPE charge per channel")
plt.show()

