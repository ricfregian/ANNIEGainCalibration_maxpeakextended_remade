# coding: utf-8

import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_context('poster')
sns.set(font_scale=1.4)

with open("../DB/TransparencyGains.json","r") as f:
    dat = json.load(f)
pdf = pd.DataFrame(dat["Gauss2"])
dat["Gauss2"].keys()

sns.pointplot(x='Date', y='c1Mu',hue='Channel',data=pdf)
plt.xlabel("Date")
plt.ylabel("SPE Charge mean (nC)")
plt.title("Mean SPE charge fits over 5 days")
plt.show()

sns.barplot(x='Channel', y='c1Mu', estimator=np.mean,data=pdf)
plt.xlabel("Channel")
plt.ylabel("SPE Charge mean (nC)")
plt.title("Mean SPE charge per channel")
plt.show()

