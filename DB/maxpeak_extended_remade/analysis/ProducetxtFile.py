import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

file = open("ChannelSPEGains2023.csv","w")

with open("combined_goodpmts.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["EXP2SPE"])
#dat["EXP2SPE"].keys()
#print(dat["EXP2SPE"].keys())

with open("combined_badpmtsrecovered.json","r") as f:
    dat = json.load(f)
badpdf = pd.DataFrame(dat["SimpleGauss"])

file.write("#Offline_Tubes: 333,346,349,352,431,444\n")
file.write("#Dead_Tubes: 337,342,345,416,445\n")
file.write("#Sinusoidal_Tubes\n")
file.write("#Channelkey,SPE_Gain\n")

badpmts = [343,359,353,366]
TUBES = np.arange(332,464,1)
for cnum in TUBES:
  if ((cnum in list(pdf["Channel"]))):
    mu = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
    L =("%i,%f\n"%(cnum,mu))
    file.write(L)
  elif ((cnum in list(badpdf["Channel"]))):
    mu = badpdf.loc[((badpdf["Channel"] == cnum)), "c1Mu"].values
    L =("%i,%f\n"%(cnum,mu))
    file.write(L)
  else:
    print("DID NOT FIND CHANNELNUM %i, MUST BE DEAD CHANNEL"%(cnum) )
    continue
file.close()
