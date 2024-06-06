# coding: utf-8

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_context('poster')
sns.set(font_scale=1.4)

#with open("../../DB/Gains2022/combined_new_gains.json","r") as f:
#with open("../../DB/gains_database.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_4.json","r") as f:
#with open("../../../gains_json_files/AmBe_gains_bkg_Gauss1_20hits_15t.json","r") as f:
with open("../../../gains_json_files/AmBe_gains_src_Gauss1_30hits_2pC.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["Gauss1"])
dat["Gauss1"].keys()

#with open("../../DB/teals_finalV_gains/combined_finalV_gains.json","r") as f:
#with open("../../DB/Gains2022/combined_new_gains.json","r") as f:
#with open("../../DB/newgains_doublestat_meanp0025.json","r") as f:
#with open("../../DB/newgains_doublestat_manual.json","r") as f:
#with open("../../DB/Gains2022_fromlowmean/gains2022.json","r") as f:
#with open("../../DB/teals_finalV_p0015_tau4s.json","r") as f:
with open("../../DB/gains_corrected/combined_corrected_fromlowmean.json","r") as f:
    dat = json.load(f)
pdf1 = pd.DataFrame(dat["EXP2SPE"])
print(dat["EXP2SPE"].keys())

'''
with open("../../DB/teals_finalV_fermi_notworking.json","r") as f:
    dat = json.load(f)
pdf1 = pd.DataFrame(dat["FERMIFIT"])
print(dat["FERMIFIT"].keys())
'''

z=(10**(-9))/(1.6*(10**(-19)))
#plt.errorbar(x='Channel', y='c1Mu', data=pdf,                     xerr = None, ls='none', marker = 'o', markersize = 6, alpha = 0.8, label = "Current SPE charge", fmt = 'o')
plt.errorbar(x='Channel', y='c1Mu', data=pdf, yerr = 'c1Mu_unc',  xerr = None, ls='none', marker = 'o', markersize = 6, alpha = 0.8, label = "AmBe source", fmt = 'o')
#plt.errorbar(x='Channel', y='c1Mu', data=pdf1, yerr = 'c1Mu_unc', xerr = None, ls='none',  marker = 'o',markersize = 6, alpha = 0.8, label = "Current gains (init. mean = 0.0015)",fmt = 'o', linewidth = 2)
plt.errorbar(x='Channel', y='c1Mu', data=pdf1, yerr = 'c1Mu_unc', xerr = None, ls='none',  marker = 'o',markersize = 6, alpha = 0.8, label = "LED on",fmt = 'o')

#plt.ylim([0.0,0.0025 ])
plt.rcParams['axes.unicode_minus'] = False #display minus sign in the axis coordinates
plt.legend(loc = "upper right")
plt.xlabel("Channel")
plt.ylabel("SPE Charge mean (nC)")
plt.title("")
plt.show()


