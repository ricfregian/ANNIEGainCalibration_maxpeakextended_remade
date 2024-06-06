import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_context('poster')
sns.set(font_scale=1.4)

#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_30hits_2pC.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_10hits_2pC_fitrng.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_10hits_2pC.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_10hits_3pC_fitrng.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_10hits_3pC.json","r") as f:
with open("../../../gains_json_files/Ambe_gains/AmBe_gains_src_Gauss1_10hits_3pC_fitrng.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_SiPMNum_SiPMhitT85_10hits_3pC_fitrng.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains/AmBeSRC_gains_Gauss1_10hits_3pC_fitrng.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["Gauss1"])
dat["Gauss1"].keys()


#with open("../../DB/gains_database.json","r") as f:
#with open("../../../gains_json_files/LEDthr_gains/LED_gains_Gauss1.json","r") as f:
#with open("../../../gains_json_files/LEDthr_gains/LEDthr_gains_Gauss1_fitrng_nrw.json","r") as f:
#with open("../../../gains_json_files/LEDthr_gains/LEDthr_gains_Gauss1_fitrng_5Runs.json","r") as f:
with open("../../../gains_json_files/LEDthr_gains/LEDthr_gains_Gauss1_fitrng_5Runs.json","r") as f:
    dat = json.load(f)
pdf1 = pd.DataFrame(dat["Gauss1"])
print(dat["Gauss1"].keys())

fig1, ax1 = plt.subplots()
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
        	ax1.errorbar(myx,myy,alpha=1.0,label="%i Data"%cnum,linestyle='None',marker='o',markersize=6)
plt.axline((0.0002, 0.0002), slope=1.0, color="black", linestyle=(0, (5, 5)))
plt.xlabel("AmBe source SPE charge (nC)")
plt.ylabel("LED SPE charge  (nC)")
plt.title("")
plt.show()

file1 = open("outliers_list.txt","a")
file2 = open("notfoundpmts_list.txt","a")
file3 = open("notfoundpmts_list_LED.txt","a")
fig2, ax2 = plt.subplots()
TUBES = np.arange(332,464,1)
for cnum in TUBES:
	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
	      print("DID NOT FIND CHANNELNUM %i IN ONE OF THE DATASET"%(cnum) )
	      file2.write("DID NOT FIND CHANNELNUM %i IN ONE OF THE DATASET \n"%(cnum) )
	      if ((cnum not in list(pdf1["Channel"]))):
	         print("DID NOT FIND CHANNELNUM %i IN LED DATASET"%(cnum) )
	         file3.write("DID NOT FIND CHANNELNUM %i IN LED DATASET \n"%(cnum) )
	      continue
	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
        	print(cnum)
        	myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
        	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
        	myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
        	yyerr = (myy/myx)*((myyerr/myy)+(myyerr/myx))
        	ax2.errorbar(cnum,myy/myx, alpha = 1.0, yerr = yyerr ,label="%i Data"%cnum,linestyle='None',marker='D',markersize=5)
        	if((myy/myx)> 1.2):
       		 print("ratio greater than 1.2 in channel: %i " %(cnum))
       		 file1.write("ratio greater than 1.2 in channel: %i \n" %(cnum))
        	if((myy/myx)< 0.8):
       		 print("ratio smaller than 0.8 in channel: %i " %(cnum))
       		 file1.write("ratio smaller than 0.8 in channel: %i \n" %(cnum))
plt.axline((320.0, 1.0), slope=0.0, color="black", linestyle=(0, (5, 5)))
plt.xlabel("Channel")
plt.ylabel("AmBe source/LED")
#plt.ylabel("AmBe source/Gains DB")
#plt.ylabel("LED/Gains DB")
plt.ylim([0.7,2.5])
plt.title("")
plt.show()

pp = []
fig4,ax4 = plt.subplots()
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
        	myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
        	yyerr = (myy/myx)*((myyerr/myy)+(myyerr/myx))
        	if(cnum > 331 and cnum < 352):
        	 ax4.errorbar(cnum,myy/myx, alpha = 1.0, yerr = yyerr ,label="%i Data"%cnum,linestyle='None',marker='D',markersize=5, markerfacecolor ="blue", markeredgecolor ="blue", ecolor="blue")
        	 #pp.append(p[0])
        	if(cnum > 351 and cnum < 372):
        	 ax4.errorbar(cnum,myy/myx, alpha = 1.0, yerr = yyerr ,label="%i Data"%cnum,linestyle='None',marker='D',markersize=5, markerfacecolor ="green", markeredgecolor ="green", ecolor="green")
        	if(cnum > 371 and cnum < 416):
        	 ax4.errorbar(cnum,myy/myx, alpha = 1.0, yerr = yyerr ,label="%i Data"%cnum,linestyle='None',marker='D',markersize=5, markerfacecolor ="brown", markeredgecolor ="brown", ecolor="brown")
        	if(cnum > 415):
        	 ax4.errorbar(cnum,myy/myx, alpha = 1.0, yerr = yyerr ,label="%i Data"%cnum,linestyle='None',marker='D',markersize=5, markerfacecolor ="black", markeredgecolor ="black", ecolor="black")
        	if((myy/myx)> 1.2):
       		 print("ratio greater than 1.2 in channel: %i " %(cnum))
#ax4.legend (pp, loc='upper left',numpoints=1)
plt.axline((320.0, 1.0), slope=0.0, color="black", linestyle=(0, (5, 5)))
plt.xlabel("Channel")
plt.ylabel("AmBe source/LED")
#plt.ylabel("AmBe source/Gains DB")
#plt.ylabel("LED/Gains DB")
plt.ylim([0.7,2.5])
plt.title("")
plt.show()
