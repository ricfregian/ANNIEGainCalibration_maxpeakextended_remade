import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_context('poster')
sns.set(font_scale=1.4)

#with open("../../DB/Gains2022/combined_new_gains.json","r") as f:
#with open("../../DB/teals_finalV_gains/combined_finalV_gains.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_30hits_2pC.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_10hits_2pC_fitrng.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_10hits_2pC.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_10hits_3pC_fitrng.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_SiPMNum_SiPMhitT85_10hits_3pC_fitrng.json","r") as f:
#with open("../../../gains_json_files/Ambe_gains/AmBe_gains_src_Gauss1_10hits_3pC_fitrng.json","r") as f:
#with open("../../../gains_json_files/LEDthr_gains/LEDthr_gains_Gauss1_fitrng_5Runs.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_src_Gauss1_10hits_3pC.json","r") as f:
#with open("../../DB/gains_corrected/combined_corrected_fromlowmean.json","r") as f:
with open("../../../gains_json_files/LEDmaxpeak_gains/LEDmaxpeak_2runs_combined.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["EXP2SPE"])
dat["EXP2SPE"].keys()
#    dat = json.load(f)
#pdf = pd.DataFrame(dat["Gauss1"])
#dat["Gauss1"].keys()


#with open("../../DB/teals_finalV_gains/combined_finalV_gains.json","r") as f:
#with open("../../DB/gains_database.json","r") as f:
#with open("../../DB/ETEL_list.json","r") as f:
#with open("../../DB/combined_all.json","r") as f:
#with open("../../DB/1part.json","r") as f:
#with open("../../DB/gains_corrected/combined_corrected_fromlowmean.json","r") as f:
with open("../../DB/maxpeak_extended/data/combined_all.json","r") as f:
    dat = json.load(f)
pdf1 = pd.DataFrame(dat["EXP2SPE"])
print(dat["EXP2SPE"].keys())

fig1, ax1 = plt.subplots()
TUBES = np.arange(332,464,1)
#TUBES = np.arange(350,375,1)
for cnum in TUBES:
	if (cnum not in list(pdf["Channel"])):
            print("DID NOT FIND CHANNELNUM %i IN EXTENDED WINDOW DATASET"%(cnum) )
            continue
	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
        	print(cnum)
        	myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
        	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
        	#myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
        	ax1.errorbar(myx,myy,alpha=1.0,label="%i Data"%cnum,linestyle='None',marker='o',markersize=6)
plt.axline((0.0002, 0.0002), slope=1.0, color="black", linestyle=(0, (5, 5)))
plt.xlabel("extended window SPE charge (nC)")
plt.ylabel("original SPE charge (nC)")
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
        	myxerr = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu_unc"].values
        	myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
        	yyerr = (myy/myx)*((myyerr/myy)+(myxerr/myx))
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
        	if((yyerr)>0.3 ):
       		 print("error greater then 0.3 in channel: %i " %(cnum))
       		 print("original dataset error : %f " %(myyerr))
       		 print("extended dataset error : %f " %(myxerr))
#ax4.legend (pp, loc='upper left',numpoints=1)
plt.axline((320.0, 1.0), slope=0.0, color="black", linestyle=(0, (5, 5)))
plt.xlabel("Channel")
plt.ylabel("original/extended")
#plt.ylabel("AmBe source/Gains DB")
#plt.ylabel("LED/Gains DB")
#plt.ylim([0.7,2.5])
plt.title("")
plt.show()


fig2, ax2 = plt.subplots()
TUBES = np.arange(332,464,1)
for cnum in TUBES:
	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
            print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
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
plt.axline((320.0, 1.0), slope=0.0, color="black", linestyle=(0, (5, 5)))
plt.xlabel("Channel")
plt.ylabel("AmBe source/LED")
#plt.ylabel("AmBe source/Gains DB")
#plt.ylabel("LED/Gains DB")
plt.ylim([0.7,2.5])
plt.title("")
plt.show()

fig3, ax3 = plt.subplots()
TUBES = np.arange(332,464,1)
for cnum in TUBES:
	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
            print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
            continue
	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
        	print(cnum)
        	myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
        	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
        	myx_peak_valley = pdf1.loc[(pdf1["Channel"] == cnum), "PV"].values
        	myx_peak_valley_unc = pdf1.loc[(pdf1["Channel"] == cnum), "PV_unc"].values
        	myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
        	yyerr = (myy/myx)*((myyerr/myy)+(myyerr/myx))
        	ax3.errorbar(myx_peak_valley,myy/myx, alpha = 1.0, yerr = myx_peak_valley_unc ,label="%i Data"%cnum,linestyle='None',marker='D',markersize=5)
        	if((myy/myx)> 1.2):
       		 print("ratio greater than 1.2 in channel: %i " %(cnum))
plt.axline((0.5, 1.0), slope=0.0, color="black", linestyle=(0, (5, 5)))
plt.xlabel("Peak to Valley ratio")
plt.ylabel("AmBe source/LED")
#plt.ylabel("AmBe source/LED")
#plt.ylabel("AmBe source/Gains DB")
#plt.ylabel("LED/Gains DB")
plt.ylim([0.7,2.5])
plt.title("")
plt.show()


fig4, ax4 = plt.subplots()
TUBES = np.arange(332,464,1)
for cnum in TUBES:
	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
            print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
            continue
	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
        	print(cnum)
        	myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
        	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
        	myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
        	yyerr = (myy/myx)*((myyerr/myy)+(myyerr/myx))
        	myx_peak_valley = pdf1.loc[(pdf1["Channel"] == cnum), "PV"].values
        	myx_peak_valley_unc = pdf1.loc[(pdf1["Channel"] == cnum), "PV_unc"].values
        	ax4.errorbar(cnum,myx_peak_valley, alpha = 1.0 ,label="%i Data"%cnum,linestyle='None',marker='D',markersize=5)
        	if((myy/myx)> 1.2):
       		 print("ratio greater than 1.2 in channel: %i " %(cnum))
#plt.axline((320.0, 1.0), slope=0.0, color="black", linestyle=(0, (5, 5)))
plt.xlabel("Channel")
plt.ylabel("Peak to Valley ratio")
#plt.ylabel("AmBe source/Gains DB")
#plt.ylabel("LED/Gains DB")
#plt.ylim([0.7,2.5])
plt.title("")
plt.show()

