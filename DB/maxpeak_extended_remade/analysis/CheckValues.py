import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_context('poster')
sns.set(font_scale=1.4)

with open("gains_database.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["EXP2SPE"])
dat["EXP2SPE"].keys()
print(dat["EXP2SPE"].keys())

badpmts = [343,359,353,366]

for cnum in badpmts:
  myy = pdf.loc[((pdf["Channel"] == cnum)), "c1Mu"].values
  #print('pmt %i , mu = %f'%(cnum)%(myy))
  print('cnum %i'%(cnum))
  print('myy',myy)

