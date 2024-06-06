import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_context('poster')
sns.set(font_scale=1.4)

with open("combined_goodpmts.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["EXP2SPE"])
print("printing keys combined_goodpmts")
print(dat["EXP2SPE"].keys())

with open("combined_badpmtsrecovered.json","r") as f:
    dat = json.load(f)
pdfbad = pd.DataFrame(dat["SimpleGauss"])
print("printing keys badpmtsrecovered")
print(dat["SimpleGauss"].keys())

#with open("gains_database_forcomparison.json","r") as f:
with open("gains_database.json","r") as f:
    dat = json.load(f)
pdf1 = pd.DataFrame(dat["EXP2SPE"])
print("printing keys gains_database")
print(dat["EXP2SPE"].keys())

TUBES = np.arange(332,464,1)
badTUBES = [343,359,353,366] 
#TUBES = np.arange(350,375,1)

pp = []
fig4,ax4 = plt.subplots()
for cnum in TUBES:
	if cnum in badTUBES:
	   if ((cnum not in list(pdfbad["Channel"])) or (cnum not in list(pdf1["Channel"]))):
               print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
               continue
	   elif((cnum in list(pdfbad["Channel"])) and (cnum in list(pdf1["Channel"]))):
           	print('plotting badpmt %i'%(cnum))
           	myy = pdfbad.loc[((pdfbad["Channel"] == cnum)), "c1Mu"].values
           	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
           	#myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
           	#myyerr = pdfbad.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
           	#yyerr = (myy/myx)*((myyerr/myy)+(myyerr/myx))
           	yyerr = 0 
	else:
	   if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
               print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
               continue
	   elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
           	print('plotting pmt %i'%(cnum))
           	myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
           	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
           	#myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
           	#myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
           	#yyerr = (myy/myx)*((myyerr/myy)+(myyerr/myx))
           	yyerr = 0 
	if(cnum > 331 and cnum < 352):
	 print(myy)
	 print(myx)
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
plt.ylabel("Extended window/Data Base")
#plt.ylabel("AmBe source/Gains DB")
#plt.ylabel("LED/Gains DB")
#plt.ylim([0.7,2.5])
plt.title("")
plt.show()




#fig3, ax3 = plt.subplots()
#TUBES = np.arange(332,464,1)
#for cnum in TUBES:
#	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
#            print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
#            continue
#	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
#        	print(cnum)
#        	myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
#        	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
#        	myx_peak_valley = pdf1.loc[(pdf1["Channel"] == cnum), "PV"].values
#        	myx_peak_valley_unc = pdf1.loc[(pdf1["Channel"] == cnum), "PV_unc"].values
#        	myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
#        	yyerr = (myy/myx)*((myyerr/myy)+(myyerr/myx))
#        	ax3.errorbar(myx_peak_valley,myy/myx, alpha = 1.0, yerr = myx_peak_valley_unc ,label="%i Data"%cnum,linestyle='None',marker='D',markersize=5)
#        	if((myy/myx)> 1.2):
#       		 print("ratio greater than 1.2 in channel: %i " %(cnum))
#plt.axline((0.5, 1.0), slope=0.0, color="black", linestyle=(0, (5, 5)))
#plt.xlabel("Peak to Valley ratio")
#plt.ylabel("AmBe source/LED")
##plt.ylabel("AmBe source/LED")
##plt.ylabel("AmBe source/Gains DB")
##plt.ylabel("LED/Gains DB")
#plt.ylim([0.7,2.5])
#plt.title("")
#plt.show()


#fig4, ax4 = plt.subplots()
#TUBES = np.arange(332,464,1)
#for cnum in TUBES:
#	if ((cnum not in list(pdf["Channel"])) or (cnum not in list(pdf1["Channel"]))):
#            print("DID NOT FIND CHANNELNUM %i IN BOTH DATASETS"%(cnum) )
#            continue
#	elif((cnum in list(pdf["Channel"])) and (cnum in list(pdf1["Channel"]))):
#        	print(cnum)
#        	myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
#        	myx = pdf1.loc[(pdf1["Channel"] == cnum), "c1Mu"].values
#        	myyerr = pdf.loc[(pdf["Channel"] == cnum), "c1Mu_unc"].values
#        	yyerr = (myy/myx)*((myyerr/myy)+(myyerr/myx))
#        	myx_peak_valley = pdf1.loc[(pdf1["Channel"] == cnum), "PV"].values
#        	myx_peak_valley_unc = pdf1.loc[(pdf1["Channel"] == cnum), "PV_unc"].values
#        	ax4.errorbar(cnum,myx_peak_valley, alpha = 1.0 ,label="%i Data"%cnum,linestyle='None',marker='D',markersize=5)
#        	if((myy/myx)> 1.2):
#       		 print("ratio greater than 1.2 in channel: %i " %(cnum))
##plt.axline((320.0, 1.0), slope=0.0, color="black", linestyle=(0, (5, 5)))
#plt.xlabel("Channel")
#plt.ylabel("Peak to Valley ratio")
##plt.ylabel("AmBe source/Gains DB")
##plt.ylabel("LED/Gains DB")
##plt.ylim([0.7,2.5])
#plt.title("")
#plt.show()


fig1, ax1 = plt.subplots()
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
plt.ylabel("LED on SPE charge  (nC)")
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
