import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import lib.Functions as fu
import numpy as np
import copy

sns.set(font_scale=1.4)


def PlotHistAndFit(xdata,ydata,function,xfit,params,fittype):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    print("POPT GOING INTO FUNC: " + str(params))
    if fittype=="Gauss1" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2])
        plt.plot(xfit,yfit,marker='None')
    if fittype=="Landau" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3])
        plt.plot(xfit,yfit,marker='None')
    if fittype=="GaussPlusExpo" and params is not None:
        yfit = fu.gauss1(xfit,params[0],params[1],params[2])
        plt.plot(xfit,yfit,marker='None')
        yfit2 = fu.expo(xfit,params[3],params[4],params[5])
        plt.plot(xfit,yfit2,marker='None') 
    if fittype=="Gauss3" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5])
        plt.plot(xfit,yfit,marker='None')
    if (fittype=="Gauss2") and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5])
        plt.plot(xfit,yfit,marker='None')
    plt.xlabel("x data")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Comparison of data and fit to data")
    plt.show()

def PlotPedestal(xdata,ydata,function,xfit,params,fittype):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    print("POPT GOING INTO FUNC: " + str(params))
    if fittype=="OrderStatPlusExpo" and params is not None:
        yfit = fu.OrderStat(xfit,params[0],params[1],params[2],
                params[3])
        plt.plot(xfit,yfit,marker='None')
        if(len(params)>3):
            yfit2 = fu.expo(xfit,params[4],params[5],params[6])
            plt.plot(xfit,yfit2,marker='None')
    if fittype=="Gauss1" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2])
        plt.plot(xfit,yfit,marker='None')
    if fittype=="GaussPlusExpo" and params is not None:
        yfit = fu.gauss1(xfit,params[0],params[1],params[2])
        plt.plot(xfit,yfit,marker='None')
        if(len(params)>3):
            yfit2 = fu.expo(xfit,params[3],params[4],params[5])
            plt.plot(xfit,yfit2,marker='None')
    if fittype=="Gauss3" and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5])
        plt.plot(xfit,yfit,marker='None')
    if (fittype=="Gauss2") and params is not None:
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5])
    if (fittype=="SPE2Peaks") and params is not None:
        #yfit = function(xfit,params[0],params[1],params[2],params[3],
        #        params[4],params[5],params[6],params[7],params[8],
        #        params[9],params[10])
        yfit = function(xfit,params[0],params[1],params[2],params[3],
                params[4],params[5],params[6],params[7],params[8])

        plt.plot(xfit,yfit,marker='None')
    plt.xlabel("Charge (nC)")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Fit of pedestal")
    plt.show()

def PlotHistPEDAndPEs(xdata,ydata,pedparams,peparams,fittype):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    yped = fu.gauss1(xdata,pedparams[0],pedparams[1],pedparams[2])
    plt.plot(xdata,yped,marker='None',label='Pedestal')
    print("PEDPARAMS ARE: " + str(pedparams))
    if len(pedparams>3):
        yexp = fu.expo(xdata,pedparams[3],pedparams[4],pedparams[5])
        plt.plot(xdata,yexp,marker='None',label='Partial amp. hits')
    y1spe = fu.gauss1(xdata,peparams[0],peparams[1],peparams[2])
    plt.plot(xdata,y1spe,marker='None',label='1PE')
    y2spe = fu.gauss1(xdata,peparams[3]*peparams[0],peparams[4]*peparams[1],peparams[5]*peparams[2])
    plt.plot(xdata,y2spe,marker='None',label='2PE')
    if fittype == "Gauss3":
       y3spe = fu.gauss1(xdata,(peparams[3]**2)*peparams[0],(peparams[4]**2)*peparams[1],(peparams[5]**2)*peparams[2])
       plt.plot(xdata,y3spe,marker='None',label='3PE')
    plt.xlabel("Charge (nC)")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Comparison of ped, PE distribution fits to data")
    leg = plt.legend(loc=1,fontsize=24)
    leg.set_frame_on(True)
    leg.draw_frame(True)
    plt.show()

def PlotHistPEDAndPEs_V2(xdata,ydata,pedparams,peparams,fittype):
    plt.plot(xdata,ydata,linestyle='None',marker='o',markersize=6)
    yped = fu.gauss1(xdata,pedparams[0],pedparams[1],pedparams[2])
    plt.plot(xdata,yped,marker='None',label='Pedestal')
    ytot = copy.deepcopy(yped)
    #if len(pedparams>3):
    #    exp_range = np.where(xdata>pedparams[1])[0]
    #    yexp = fu.expo(xdata[exp_range],pedparams[3],pedparams[4],pedparams[5])
    #    ytot[exp_range] = ytot[exp_range]+yexp
    #    plt.plot(xdata[exp_range],yexp,marker='None',label='Partial amp. hits')
    if fittype in ["SimpleGauss"]:
        y1spe = fu.SimpleGauss(xdata,peparams[0],peparams[1],peparams[2])
        #Gian
        for i, element in enumerate (xdata):
         if element<(pedparams[1]+pedparams[2]):
          y1spe[i]=0
        ####
        ytot = ytot+y1spe
        plt.plot(xdata,y1spe,marker='None',label='1PE')
    if fittype in ["SPE","SPE2Peaks","SPE3Peaks","EXP2SPE","EXP3SPE"]:
        y1spe = fu.SPEGaussians_NoExp(xdata,peparams[0],peparams[1],peparams[2],peparams[3],peparams[4],
                peparams[5])
        #Gian
        for i, element in enumerate (xdata):
         if element<(pedparams[1]+pedparams[2]):
          y1spe[i]=0
        ####
        ytot = ytot+y1spe
        plt.plot(xdata,y1spe,marker='None',label='1PE')
    if fittype in ["SPE2Peaks","EXP2SPE","EXP3SPE"]:
        y2spe = fu.gauss1(xdata, peparams[6]*peparams[0]*(1+peparams[3]), 
                                 peparams[1]*(1+peparams[4]),peparams[2]*np.sqrt(1+(peparams[5]**2))) + \
                fu.gauss1(xdata, peparams[6]*2*peparams[0],2*peparams[1],peparams[2]*np.sqrt(2))
        #Gian
        for i, element in enumerate (xdata):
         if element<(pedparams[1]+pedparams[2]):
          y2spe[i]=0
        ####
        ytot = ytot+y2spe
        plt.plot(xdata,y2spe,marker='None',label='2PE')
    if fittype in ["EXP3SPE"]:
        y3spe = fu.gauss1(xdata, peparams[10]*3*peparams[6]*peparams[0], 
                                 3*peparams[1],np.sqrt(3)*peparams[2])
        ytot = ytot+y3spe
        plt.plot(xdata,y3spe,marker='None',label='3PE')
    if fittype in ["EXP2SPE","EXP3SPE"]:
        #Gian
        yexp = fu.expo(xdata, peparams[7],peparams[8],peparams[9])
        #expxdata = xdata
        #yexp = fu.expo(expxdata, peparams[7],peparams[8],peparams[9])
        #Gian
        for i, element in enumerate (xdata):
         if element<(pedparams[1]+pedparams[2]):
          yexp[i]=0
        plt.plot(xdata,yexp,marker='None',label='Exponential')
        ytot = ytot + yexp
    if fittype=="SPE3Peaks":
        y2spe = fu.gauss1(xdata, peparams[6]*peparams[0]*(1+peparams[3]), 
                                 peparams[1]*(1+peparams[4]),peparams[2]*np.sqrt(1+(peparams[5]**2))) + \
                fu.gauss1(xdata, peparams[6]*2*peparams[0],peparams[1]*2*peparams[1],peparams[2]*np.sqrt(2))
        ytot = ytot+y2spe
        plt.plot(xdata,y2spe,marker='None',label='2PE')
        y3spe = fu.gauss1(xdata, peparams[7]*peparams[0]*(2+peparams[3]), 
                                 peparams[1]*(2+peparams[4]),peparams[2]*np.sqrt(2+(peparams[5]**2))) + \
                fu.gauss1(xdata, peparams[7]*3*peparams[0],peparams[1]*3*peparams[1],peparams[2]*np.sqrt(3))
        ytot = ytot+y3spe
        plt.plot(xdata,y3spe,marker='None',label='3PE')
    #Gian
    plt.axvline(x=(pedparams[1]+pedparams[2]), color="black", linestyle="--", linewidth = 3) 
    plt.plot(xdata,ytot,marker='None',label='Total Fit')
    plt.xlabel("Charge (nC)")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Comparison of ped, PE distribution fits to data")
    leg = plt.legend(loc=1,fontsize=24)
    leg.set_frame_on(True)
    leg.draw_frame(True)
    #plt.savefig("exp2spe.pdf")
    plt.show()

def PlotDataAndSPEMean(tot_hist_data,totped_fit, bkg_hist_data,bkgped_fit,SPEMean):
    plt.plot(tot_hist_data["bins"],tot_hist_data["bin_heights"],linestyle='None',marker='o',markersize=7,label='signal data')
    TotalToBkgPedRatio = totped_fit['popt'][0]/bkgped_fit['popt'][0]
    plt.plot(bkg_hist_data["bins"],bkg_hist_data["bin_heights"]*TotalToBkgPedRatio,linestyle='None',marker='o',markersize=7,label='scaled bkg data')
    plt.axvline(x=SPEMean,linewidth=4,label='SPE Estimate')
    plt.xlabel("Charge (pC)")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Fermi method SPE estimation compared with data")
    leg = plt.legend(loc=1,fontsize=24)
    leg.set_frame_on(True)
    leg.draw_frame(True)
    plt.show()

def PlotDataAndSPEMean_NoFit(tot_hist_data, bkg_hist_data,SPEMean,PED_CUTOFF):
    plt.plot(tot_hist_data["bins"],tot_hist_data["bin_heights"],linestyle='None',marker='o',markersize=7,label='signal data')
    TotalToBkgPedRatio = np.sum(tot_hist_data['bin_heights'])/np.sum(bkg_hist_data['bin_heights'])
    plt.plot(bkg_hist_data["bins"],bkg_hist_data["bin_heights"]*TotalToBkgPedRatio,linestyle='None',marker='o',markersize=7,label='scaled bkg data')
    plt.axvline(x=SPEMean,linewidth=4,label='SPE Estimate')
    plt.axvline(x=PED_CUTOFF,linewidth=4,label='Pedestal Cut',color='red')
    plt.xlabel("Charge (pC)")
    plt.ylabel("Entries")
    plt.ylim(ymin=0.9)
    plt.yscale("log")
    plt.title("Fermi method SPE estimation compared with data")
    leg = plt.legend(loc=1,fontsize=24)
    leg.set_frame_on(True)
    leg.draw_frame(True)
    plt.show()
