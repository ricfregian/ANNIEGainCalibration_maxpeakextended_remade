import numpy as np
import scipy as sp
import scipy.optimize as scp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import json

DATADIR = "../DB/tealsV3_fromlowmean/"

if __name__=='__main__':
    gain_files = glob.glob(DATADIR+"*.json")
    df = None
    for f in gain_files:
        dat = None
        with open(f,"r") as f:
            dat = json.load(f)
            if df is None:
                df = pd.DataFrame(dat["EXP2SPE"])
            else:
                df = pd.concat([df,pd.DataFrame(dat["EXP2SPE"])],axis=0)
    print(df)
    with open("tealsV3_combined_fromlowmean.json","w") as f:
        json.dump(df.to_dict('list'),f,indent=4)
