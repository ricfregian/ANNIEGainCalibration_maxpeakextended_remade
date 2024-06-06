import numpy as np
import scipy as sp
import scipy.optimize as scp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import json

off_list_database=[333,346,349,352,431,444]
nogains_list = [343,337,342,345,359,416,445,353,366]
#FILEPATH = "combined_all_forcomparison.json"
FILEPATH = "gains_database_forcomparison.json"
#CHANSTOREMOVE = [353,355]
CHANSTOREMOVE = nogains_list

if __name__=='__main__':
    with open(FILEPATH,"r") as f:
        dat = json.load(f)
    df = pd.DataFrame(dat["EXP2SPE"])
    for chan in CHANSTOREMOVE:
        todrop = df[df['Channel'] == chan].index
        df.drop(todrop, inplace=True)
    
    with open("channels_removed.json","w") as f:
        json.dump(df.to_dict('list'),f,indent=4)
