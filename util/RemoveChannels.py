import numpy as np
import scipy as sp
import scipy.optimize as scp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import json

FILEPATH = "./SimpleGainCurves_HV.json"
CHANSTOREMOVE = [353,355]

if __name__=='__main__':
    with open(FILEPATH,"r") as f:
        dat = json.load(f)
    df = pd.DataFrame(dat)
    for chan in CHANSTOREMOVE:
        todrop = df[df['Channel'] == chan].index
        df.drop(todrop, inplace=True)
    
    with open("SimpleGainCurves_GoodFits.json","w") as f:
        json.dump(df.to_dict('list'),f,indent=4)
