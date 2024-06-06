import numpy as np
import json
import ROOT
import sys
import matplotlib.pyplot as plt

import lib.ArgParser as ap
import lib.Functions as fu
import lib.GainFinder as gf
import lib.FermiFitter as ff
import lib.ParamInput as pin
import lib.Plots as pl

HIST_TITLETEMPLATE = "hist_charge_CNUM" #FIXME: Make a configurable somehow
#loop through each channel, show the histogram, and ask whether to use 
#Default fitting params

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)


if __name__=='__main__':
    print(" ###### WELCOME TO ANNIE GAIN CALIBRATION ###### ")
    if ap.APPEND is not None:
        print(" ####### APPENDING NEW INFO TO GAIN DATABASE ####### ")
    with open(ap.APPEND,"r") as f:
        myfile = ROOT.TFile.Open(ap.APPEND)
    if ap.BKG is not None:
        print(" ####### LOADING BACKGROUND RUN FOR USE IN FERMI FITTER ####### ")
        with open(ap.BKG,"r") as f:
            bkgfile = ROOT.TFile.Open(ap.BKG)

    #FIXME: have this be a configurable or a file path added by user
    #with open("./DB/TranspChannels.txt","r") as f:
    #    chans = f.readlines()
    #    for j,l in enumerate(chans):
    #        chans[j]=int(chans[j].rstrip("\n"))
    #channel_list = np.array(chans)
    #off_list = [333,342,345,346,349,352,359,374,394,431,444,445]
    #channel_list = np.array([360,365])

    
    #chunks of channels
    #channel_list = np.arange(332,352)
    #channel_list = np.arange(352,400)
    #channel_list = np.arange(400,464)
    
    #badpmts
    channel_list = [343,359,353,366]
    channel_list = [353] # needed fit from pedmean-5*pedsigma

    #chunks without ETEL
    #channel_list = np.arange(332,350)
    #channel_list = np.arange(376,400)

    #all channels
    #channel_list = np.arange(332,464) 
  
    #off channels database
    off_list_database=[333,346,349,352,431,444]
    #nogains_list = [343,337,342,345,359,416,445]
    #new nogains_list
    nogains_list = [343,337,342,345,359,416,445,353,366]
    
    ETEL_list = [350,351,353,354,355,356,357,358,359,360,361,362,363,364,365,366,367,368,369,370,371,372,373,374,375]
  
    #channel_list = np.setdiff1d(channel_list,off_list_database)
    #channel_list = np.setdiff1d(channel_list,nogains_list)

    #channel_list = [343,337,342,345,359,416,445,353,366]

    #Load dictionary of initial fit parameters
    with open("./DB/InitialParams.json","r") as f:
        init_params = json.load(f)

    #if ap.FIT == "Simple":
    #    fittype = str(input("Fit type to perform to PE peaks (Gauss2, Gauss3,SPE,EXP2SPE,EXP3SPE,SPE2Peaks,SPE3Peaks): "))
    #    if fittype not in ["Gauss2","Gauss3","SPE","SPE2Peaks","SPE3Peaks","EXP2SPE","EXP3SPE"]:
    #        print("Please input a valid fitting approach to take.")
    #        sys.exit(0)

    if ap.FIT == "Simple":
        #fittype = str("EXP2SPE") #Gian discover
        #print("using EXP2SPE for PEPeaks")
        fittype = str("SimpleGauss") #for badpmts
        print("using SimpleGauss")
        #fittype = str("SPE") #for badpmts
        #print("using SPE")

    if ap.FIT == "FERMI":
        fittype = "FERMIFIT"

    with open(ap.DB) as dbfile:
        db = json.load(dbfile)
        fitdata = db[fittype]
        dbfile.close()

    if ap.FIT == "Simple":
        #Initialize Gain-Fitting class
        GainFinder = gf.GainFinder(myfile)
        if(fittype == "Gauss2"):
            GainFinder.setFitFunction(fu.gauss2dep)
            GainFinder.setInitialFitParams(init_params["GaussDepInitParams"])
            GainFinder.setBounds(init_params["GaussDepLB"],init_params["GaussDepUB"])
        if(fittype == "Gauss3"):
            GainFinder.setFitFunction(fu.gauss3dep)
            GainFinder.setInitialFitParams(init_params["GaussDepInitParams"])
            GainFinder.setBounds(init_params["GaussDepLB"],init_params["GaussDepUB"])
        if(fittype == "SPE"):
            GainFinder.setFitFunction(fu.SPEGaussians_NoExp)
            GainFinder.setInitialFitParams(init_params["SPEInitParams"])
            GainFinder.setBounds(init_params["SPELB"],init_params["SPEUB"])
        if(fittype == "SPE2Peaks"):
            GainFinder.setFitFunction(fu.SPE2Peaks)
            GainFinder.setInitialFitParams(init_params["SPE2PeaksInitParams"])
            GainFinder.setBounds(init_params["SPE2PeaksLB"],init_params["SPE2PeaksUB"])
        if(fittype == "SPE3Peaks"):
            GainFinder.setFitFunction(fu.SPE3Peaks)
            GainFinder.setInitialFitParams(init_params["SPE3PeaksInitParams"])
            GainFinder.setBounds(init_params["SPE3PeaksLB"],init_params["SPE3PeaksUB"])
        if(fittype == "EXP2SPE"):
            GainFinder.setFitFunction(fu.EXP2SPE)
            GainFinder.setInitialFitParams(init_params["EXP2SPEInitParams"])
            GainFinder.setBounds(init_params["EXP2SPELB"],init_params["EXP2SPEUB"])
        if(fittype == "EXP3SPE"):
            GainFinder.setFitFunction(fu.EXP3SPE)
            GainFinder.setInitialFitParams(init_params["EXP3SPEInitParams"])
            GainFinder.setBounds(init_params["EXP3SPELB"],init_params["EXP3SPEUB"])
        if(fittype == "SimpleGauss"):
            GainFinder.setFitFunction(fu.SimpleGauss)
            GainFinder.setInitialFitParams(init_params["SimpleGauss"])
            GainFinder.setBounds(init_params["SGaussLB"],init_params["SGaussUB"])


        #Loop through channels in file and fit gains to each
        for channel_num in channel_list:
            print("--------- FITTING FOR CHANNEL %i ----------"%(channel_num))
            thehist = HIST_TITLETEMPLATE.replace("CNUM",str(channel_num))
            if not myfile.GetListOfKeys().Contains(thehist):
                print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
                continue
           

            #Fit photoelectron peaks
            FIT_TAIL = False
            FitComplete = False
            PedFitComplete = False
            GoodPedFit = False
            exp_fit_range = []
            while not PedFitComplete:
                #Fit pedestal and exponential tail from failed dynode hits
                print("PEDESTAL PARAMS: " + str(init_params["PedParams"]))
                pedopt,pedcov,pedxdata,pedydata,pedyunc = GainFinder.FitPedestal(
                        thehist, init_params["PedParams"],init_params["PedFitRange"],
                        fit_tail = FIT_TAIL, exp_fit_range = exp_fit_range)
                if pedopt is None:
                    print("PEDESTAL FIT FULLY FAILED... LIKELY A BUNK CHANNEL.  SKIPPING")
                    PedFitComplete = True
                    GoodPedFit = False
                    FitComplete = True
                    GoodFit = False
                    continue
                pl.PlotPedestal(pedxdata,pedydata,fu.gauss1,pedxdata,pedopt,"GaussPlusExpo")
                above_ped = 0
                past_ped = np.where(pedxdata > (pedopt[1] + 3*pedopt[2]))[0]
                if FIT_TAIL:
                    plt.plot(pedxdata[past_ped],pedydata[past_ped])
                    plt.plot(pedxdata[past_ped],fu.expo(pedxdata[past_ped],pedopt[3],
                                       pedopt[4],pedopt[5]))
                    above_ped = np.sum(pedydata[past_ped] - fu.expo(pedxdata[past_ped],pedopt[3],
                                       pedopt[4],pedopt[5]))
                else:
                    above_ped = np.sum(pedydata[past_ped] - fu.gauss1(pedxdata[past_ped],pedopt[0],
                                      pedopt[1],pedopt[2]))
                #plt.show() #Gian
                print("4SIGMA PAST PED, EXP. SUBTRACTED: " + str(above_ped))
                if (above_ped < 300):
                    print("Low statistics beyond pedestal!  May just be fitting on fluctuations.")
                    skip_fit = str(input("Skip this fit?"))
                    if skip_fit in ["y","Y","yes","Yes","YES"]:
                        PedFitComplete = True
                        GoodPedFit = False
                        FitComplete = True
                        GoodFit = False
                        continue

                ped_good = str(input("Happy with pedestal fit? [y/N]:"))
                #ped_good = "yes" #Gian
                if ped_good in ["y","Y","yes","Yes","YES"]:
                    PedFitComplete = True
                    GoodPedFit = True
                else:
                    if FIT_TAIL:
                        fit_min = str(input("Exponential window min: "))
                        fit_max = str(input("Exponential window max: "))
                        exp_fit_range = [float(fit_min),float(fit_max)]

            UseDefault = "y"

            while not FitComplete:
                print("while not FitComplete")
                print("SIGMA LIMIT IS: " + str(pedopt[2]))
                #####setTauMax must be used for EXP2SPE 
                #####setTauMax not used for simple SimpleGauss 
                if (fittype == str("EXP2SPE")):
                   print("Setting TauMax")
                   GainFinder.setTauMax((pedopt[2]/2)) # Gian
                #GainFinder.setTauMax(6*pedopt[2]) # Gian
                #GainFinder.setTauMax(2*pedopt[2]) # Gian
                #GainFinder.setTauMax(4*pedopt[2]) # Gian
                #GainFinder.setTauMax(pedopt[2]) # Gian
                #GainFinder.setTMin(pedopt[1]) # Gian
                #GainFinder.setTMax(4*pedopt[2]) # Gian
                init_mean = str(input("Guess at SPE mean: "))
                #editing so the code doesn't ask for the mean : #Gian
                #init_mean = 0.001
                if(float(init_mean) >=0.006  and fittype == str("EXP2SPE")):
                    print("TRY LESS THAN 0.006")
                    continue
                try:
                    GainFinder.setInitMean(float(init_mean)) # this is changing the mean of the init params, which will be used in the FitPEPeaks 
                except ValueError:
                    print("Input not recognized.  Trying a save bet of 0.001")
                    GainFinder.setInitMean(0.001)
                if UseDefault in ["y","Y","yes","Yes","YES"]:
                    popt,pcov,xdata,ydata,y_unc = GainFinder.FitPEPeaks(thehist,
                            exclude_ped = True,subtract_ped = True)
                elif UseDefault in ["n","N","No","no","NO"]:
                    InitialParams = pin.GetInitialParameters(fittype)
                    popt,pcov,xdata,ydata,y_unc = GainFinder.FitPEPeaks(thehist)
                if popt is None:
                    print("FIT FAILED.  WE'RE MOVING ON TO THE NEXT CHANNEL")
                    FitComplete = True
                    GoodFit = False
                    continue
                print("BEST FIT PARAMS FROM FitPEPeaks: " + str(popt))
                #pl.PlotHistAndFit(xdata,ydata,GainFinder.fitfunc,xdata,popt,fittype)
                #print("Presenting combined final fit")
                #pl.PlotHistPEDAndPEs(xdata,ydata,pedopt,popt,fittype)
                pl.PlotHistPEDAndPEs_V2(xdata,ydata,pedopt,popt,fittype)
                if popt is None:
                    retry_fit = str(input("Fit failed! Retry? [y/N]: "))
                    if retry_fit not in ["y","Y","yes","Yes","YES"]:
                        FitComplete = True
                        continue
                    else:
                        UseDefault = str(input("Use default fit parameters? [y/N]"))
                approve_fit = str(input("Fit converged! Happy with this fit? [y/N]: "))
                #approve_fit = "yes"#Gian
                if approve_fit in ["y","Y","yes","Yes","YES"]:
                    FitComplete = True
                    GoodFit = True
                else:
                    retry = str(input("Try again? [y/N]: "))
                    if retry not in ["y","Y","yes","Yes","YES"]:
                        FitComplete = True
                        GoodFit = False

            if GoodFit:
                print("With the pedestal and 1PE peak fit, estimate the PV ratio")
                print("pedestal mean :"+ str(pedopt[1]))
                print("1PE peak mean:"+ str(popt[1]))
                Valley_inds = np.where((xdata>pedopt[1]) & (xdata<popt[1]))[0]
                print("valley bins:" + str(Valley_inds))
                Valley_min = np.argmin(ydata[Valley_inds])
                print("VALLEY MIN AT BIN: " + str(xdata[Valley_min]))
                Valley_estimate_bins = ydata[np.arange(Valley_min-1,Valley_min+4,1)]
                Valley_estimate = np.average(Valley_estimate_bins)
                print("VALLEY MEAN ESTIMATE: " + str(Valley_estimate))
                V_unc = np.std(Valley_estimate_bins)
                Peak_max = np.abs(xdata-popt[1]).argmin()
                print("PEAK MAX AT BIN: " + str(xdata[Peak_max]))
                Peak_estimate_bins = ydata[np.arange(Peak_max-2,Peak_max+3,1)]
                Peak_estimate = np.average(Peak_estimate_bins)
                print("PEAK MEAN ESTIMATE: " + str(Peak_estimate))
                P_unc = np.std(Peak_estimate_bins)
                print("P/V RATIO ESTIMATE: " + str(Peak_estimate/Valley_estimate))
                PV_unc = (Peak_estimate/Valley_estimate)*np.sqrt((1/V_unc)**2 + (1/P_unc)**2)
                print("P/V RATIO UNC: " + str(PV_unc))


                #Since we've made it out, save to the DB
                db[fittype]["Channel"].append(channel_num)
                #db[fittype]["RunNumber"].append(ap.RUNNUM)
                #db[fittype]["LEDsOn"].append(ap.LED)
                #db[fittype]["LEDPINs"].append(ap.PIN)
                #db[fittype]["Date"].append(ap.DATE)


                #print("appending volts %i"%(int(ap.VOLTS)))
                #db[fittype]["V"].append(int(ap.VOLTS)) #gian
                db[fittype]["PV"].append(Peak_estimate/Valley_estimate)#gian
                db[fittype]["PV_unc"].append(PV_unc)#gian
                errs = np.sqrt(np.diag(pcov))
                #if fittype in ["Gauss2","Gauss3"]:
                #    db[fittype]["c1Height"].append(popt[0])#gian
                #    db[fittype]["c1Mu"].append(popt[1])#gian
                #    db[fittype]["c1Sigma"].append(popt[2])#gian
                #    db[fittype]["c2HScale"].append(popt[3])#gian
                #    db[fittype]["c2MScale"].append(popt[4])#gian
                #    db[fittype]["c2SScale"].append(popt[5])#gian
                #    db[fittype]["c1Height_unc"].append(errs[0])#gian
                #    db[fittype]["c1Mu_unc"].append(errs[1])#gian
                #    db[fittype]["c1Sigma_unc"].append(errs[2])#gian
                #    db[fittype]["c2HScale_unc"].append(errs[3])#gian
                #    db[fittype]["c2MScale_unc"].append(errs[4])#gian
                #    db[fittype]["c2SScale_unc"].append(errs[5])#gian
                if fittype in ["SimpleGauss"]:
                    db[fittype]["c1Height"].append(popt[0])
                    db[fittype]["c1Mu"].append(popt[1])
                    db[fittype]["c1Sigma"].append(popt[2])
                    db[fittype]["c1Height_unc"].append(errs[0])
                    db[fittype]["c1Mu_unc"].append(errs[1])
                    db[fittype]["c1Sigma_unc"].append(errs[2])
                if fittype in ["SPE2Peaks","EXP2SPE","EXP3SPE"]:
                    db[fittype]["c1Height"].append(popt[0])
                    db[fittype]["c1Mu"].append(popt[1])
                    db[fittype]["c1Sigma"].append(popt[2])
                    db[fittype]["c2HScale"].append(popt[3])
                    db[fittype]["c2MScale"].append(popt[4])
                    db[fittype]["c2SScale"].append(popt[5])
                    db[fittype]["SCScale"].append(popt[6])
                    db[fittype]["c1Height_unc"].append(errs[0])
                    db[fittype]["c1Mu_unc"].append(errs[1])
                    db[fittype]["c1Sigma_unc"].append(errs[2])
                    db[fittype]["c2HScale_unc"].append(errs[3])
                    db[fittype]["c2MScale_unc"].append(errs[4])
                    db[fittype]["c2SScale_unc"].append(errs[5])
                    db[fittype]["SCScale_unc"].append(errs[6])
                if fittype in ["EXP2SPE","EXP3SPE"]:
                    db[fittype]["CExp"].append(popt[7])
                    db[fittype]["f_mu"].append(popt[8])
                    db[fittype]["tau"].append(popt[9])
                    db[fittype]["CExp_unc"].append(errs[7])
                    db[fittype]["f_mu_unc"].append(errs[8])
                    db[fittype]["tau_unc"].append(errs[9])
        with open(ap.DB,"w") as dbfile:
            print("opening DB:")
            json.dump(db,dbfile, cls=NpEncoder,sort_keys=False, indent=4)
            print("after writing DB")

    if ap.FIT == "FERMI":
        print("TRYING FERMI FIT")
        #Loop through channels in file and fit gains to each
        FermiFitter = ff.FermiFitter()
        for channel_num in channel_list:
            print("FITTING FOR CHANNEL %i"%(channel_num))
            thehist = HIST_TITLETEMPLATE.replace("CNUM",str(channel_num))
            if not myfile.GetListOfKeys().Contains(thehist):
                print("HISTOGRAM %s NOT FOUND.  SKIPPING"%(thehist))
                continue
          
            #Get the histogram data in numpy array format
            tot_hist_data = FermiFitter.ProcessHistogram(myfile,thehist)
            bkg_hist_data = FermiFitter.ProcessHistogram(bkgfile,thehist)

            FitComplete = False
            GoodFit = False
            TotPedFitComplete = False
            TotGoodPedFit = False
            BkgPedFitComplete = False
            BkgGoodPedFit = False
            fit_range = init_params["PedFitRange"]
            SPEMean = None
            SPEVariance = None
            SPEMeanErr = None
            ped_fit = FermiFitter.FitPedestal(bkg_hist_data,init_params["PedParams"],init_params["PedFitRange"])
            if ped_fit['popt'] is not None:
                PED_CUTOFF = ped_fit['popt'][1] + 4*ped_fit['popt'][2]
            else:
                print("NO GOOD PED FIT.  SETTING PED CUTOFF OF 0.0002")
                PED_CUTOFF = 0.00025
            while not FitComplete:
                SPEMean = FermiFitter.EstimateSPEMean(tot_hist_data,bkg_hist_data,PED_CUTOFF)
                print("SPE MEAN ESTIMATE: " + str(SPEMean))
                SPEVariance = FermiFitter.EstimateSPEVariance(tot_hist_data,bkg_hist_data,PED_CUTOFF)
                print("SPE VARIANCE ESTIMATE: " + str(SPEVariance))
                SPEMeanErr = FermiFitter.EstimateSPEError(tot_hist_data,bkg_hist_data,PED_CUTOFF)
                print("SPE ERROR ESTIMATE: " + str(SPEMeanErr))
                #pl.PlotDataAndSPEMean(tot_hist_data,totped_fit,bkg_hist_data,bkgped_fit,SPEMean)
                pl.PlotDataAndSPEMean_NoFit(tot_hist_data,bkg_hist_data,SPEMean,PED_CUTOFF)
                fit_good = str(input("Happy with this final fit? [y/N]:"))
                if fit_good in ["y","Y","yes","Yes","YES"]:
                    FitComplete = True
                    GoodFit = True
                else:
                    print("That's too bad... continuing")
                    FitComplete = True
            #Now, we save the results
            if GoodFit:
                #With the pedestal and 1PE peak fit, estimate the PV ratio
                db[fittype]["Channel"].append(channel_num)
                db[fittype]["RunNumber"].append(ap.RUNNUM)
                db[fittype]["LEDsOn"].append(ap.LED)
                db[fittype]["LEDPINs"].append(ap.PIN)
                db[fittype]["Date"].append(ap.DATE)
                db[fittype]["V"].append(int(ap.VOLTS))
                db[fittype]["c1Mu"].append(SPEMean)
                db[fittype]["c1Mu_unc"].append(SPEVariance)
                db[fittype]["c1Mu_StdErr"].append(SPEMeanErr)
        with open(ap.DB,"w") as dbfile:
            json.dump(db,dbfile,sort_keys=False, indent=4)

print("end of main.py")
