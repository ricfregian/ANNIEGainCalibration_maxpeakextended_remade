import numpy as np
import scipy as sp
import scipy.optimize as scp
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import glob
import json

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

sns.set_context("poster")

#DATADIR = "../DB/GainFits/"
DATADIR = "../DB/teals_finalV_gains/"

def expo(x,A,l,C):
    return A*np.exp(x/l) + C

def ChargeToV(Q,A,l,C):
    return l*np.log((Q-C)/A)

if __name__=='__main__':
    gain_files = glob.glob(DATADIR+"*.json")
    df = None
    for f in gain_files:
        dat = None
        with open(f,"r") as f:
            dat = json.load(f)
            if df is None:
                #df = pd.DataFrame(dat)#["EXP2SPE"])
                df = pd.DataFrame(dat["EXP2SPE"])
            else:
                #df = pd.concat([df,pd.DataFrame(dat)],axis=0) #["EXP2SPE"])],axis=0)
                df = pd.concat([df,pd.DataFrame(dat["EXP2SPE"])],axis=0)
    print(df)

    TUBES = np.array(list(set(df["Channel"])))
    TUBES = np.arange(332,464,1)
    results = {"Channel":[], "Setpoint":[]}
    failures = {"Channel":[]}
    for cnum in TUBES:
        if cnum not in list(df["Channel"]):
            print("DID NOT FIND ANY DATA FOR CHANNELNUM %i"%(cnum))
            failures["Channel"].append(cnum)
            continue
        fig,ax = plt.subplots()
        print(cnum)
        myx = df.loc[((df["Channel"] == cnum)), "PV"].values
        myy = df.loc[(df["Channel"] == cnum), "c1Mu"].values*(6.2415E9)
        myyerr = df.loc[(df["Channel"] == cnum), "c1Mu_unc"].values*(6.2415E9)
        #myx = df.loc[((df["Channel"] == cnum) & ((df["c1Mu"]>0.0006) | (df["c1Height"]>100))), "V"]
        #myy = df.loc[((df["Channel"] == cnum) & ((df["c1Mu"]>0.0006) | (df["c1Height"]>100))), "c1Mu"]*(6.2415E9)
        #myyerr = df.loc[((df["Channel"] == cnum) & ((df["c1Mu"]>0.0006) | (df["c1Height"]>100))), "c1Mu_unc"]*(6.2415E9)
        print(myx)
        print(myy)
        if (len(myx)<3):
            print("Not enough data to fit an exponential.")
            print("SKIPPING CHANNEL %i"%(cnum))
            failures["Channel"].append(cnum)
            continue
        ax.errorbar(myx,myy,yerr=myyerr,alpha=0.8,label="%i Data"%cnum,linestyle='None',marker='o',markersize=6)
        #ax.bar(y = myy,x = range(len(myx)), yerr = myyerr,label = cnum)
        #ax.xticks(range(len(myx)),myx)
        init_params = [5E5,100,1000]
        try:
            popt, pcov = scp.curve_fit(expo, myx, myy,p0=init_params, sigma=myyerr, maxfev=12000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT FOR CHANNEL %i"%(cnum))
            failures["Channel"].append(cnum)
            continue
        ax.plot(np.sort(myx),expo(np.sort(myx),popt[0],popt[1],popt[2]),label='Exponential Fit')
        print("CHANNEL: %i"%(cnum))
        print("1E7 GAIN VOLTAGE: %s"%(str(ChargeToV(1E7,popt[0],popt[1],popt[2]))))
        print("5E6 GAIN VOLTAGE: %s"%(str(ChargeToV(5E6,popt[0],popt[1],popt[2]))))
        results["Channel"].append(cnum)
        results["Setpoint"].append(ChargeToV(1E7,popt[0],popt[1],popt[2]))
        leg = ax.legend(loc=2,fontsize=15)
        leg.set_frame_on(True)
        leg.draw_frame(True)
        ax.set_xlabel("Voltage") 
        ax.set_ylabel("SPE Charge Fit") 
        plt.xticks(rotation='30',fontsize=10)
        plt.title(("Best fit to SPE distribution"))
        plt.show()
    g = sns.FacetGrid(df,col='Channel',col_wrap=2,ylim=(0,0.002))
    g.map(sns.pointplot,"PV","c1Mu",color=".3",ci=None)
    plt.savefig("GainPlots.pdf")
    print(results)
    print(failures)
    with open("FitVoltages.json","w") as f:
        json.dump(results,f,cls=NpEncoder,indent=4)
    with open("FailedFits.json","w") as f:
        json.dump(failures,f,cls=NpEncoder,indent=4)
        json.dump(results,f,cls=NpEncoder,indent=4)
