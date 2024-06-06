import scipy.optimize as scp
import numpy as np
import lib.Functions as fu
import copy
import matplotlib.pyplot as plt

class GainFinder(object):
    def __init__(self, ROOTFile):
        self.ROOTFile = ROOTFile
        self.initial_params = []
        self.hist_string = "hist_charge_CNUM"

        self.ped_mean = None
        self.ped_sigma = None
        self.ped_fit_y = None
        self.ped_fit_y_un = None
        self.ped_fit_x = None

        self.fitfunc = None
        self.lower_bounds = None
        self.upper_bounds = None


    def setFitFunction(self,fitfunc):
        self.fitfunc = fitfunc
    
    def setInitialFitParams(self,initial_params):
        self.initial_params =  initial_params

    def setInitMean(self,mean):
        self.initial_params[1] = mean #FIXME: This is specific to how gauss1 is defined. generalize
    
    def setTauMax(self,tau):
        print("TAU MAX WILL BE: " + str(tau))
        self.upper_bounds[8] = tau #FIXME: This is specific to how gauss1 is defined. generalize
        #self.upper_bounds = tau #FIXME: This is specific to how gauss1 is defined. generalize# Gian

    #Gian
    def setTMin(self,t):
        print("MIN T BOUND WILL BE: " + str(t))
        self.lower_bounds[9] = t

    def setTMax(self,t):
        print("MIN T BOUND WILL BE: " + str(t))
        self.upper_bounds[9] = t

    def setBounds(self,lower_bounds,upper_bounds):
        self.lower_bounds =  lower_bounds
        self.upper_bounds =  upper_bounds

    def FitPedestal(self,HistName,init_params,fit_range,fit_tail=False,exp_fit_range=[]):
        '''
        Uses a Gaussian from the Functions library to attempt to fit
        the pedestal peak of the distribution.  A fit range can be
        given if helping down-select to the pedestal-dominant region.

        Inputs:

        HistName [string]
            string of histogram name in self.ROOTFile.

        init_params [array]
            Initial parameters to try fitting a single gaussian with.
            Format is [amplitude,mean,sigma].

        fit_range [array]
            Range of values to perform fit across.  Helps to down-select
            to the ped-only range.
        '''
        print("FITTING TO PEDESTAL NOW")
        thehist =  self.ROOTFile.Get(HistName)
        #Get histogram information into ntuples
        bin_centers, evts,evts_unc =(), (), () #pandas wants ntuples
        fit_bin_centers, fit_evts,fit_evts_unc =(), (), () #pandas wants ntuples
        ped_indices = []
        for i in range(int(thehist.GetNbinsX()+1)):
            if i==0:
                continue
            bin_centers =  bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            evts = evts + (thehist.GetBinContent(i),)
            evts_unc = evts_unc + (thehist.GetBinError(i),)
            fit_bin_centers =  fit_bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            fit_evts = fit_evts + (thehist.GetBinContent(i),)
            fit_evts_unc = fit_evts_unc + (thehist.GetBinError(i),)
        bin_centers = np.array(bin_centers)
        evts = np.array(evts)
        evts_unc = np.array(evts_unc)
        fit_bin_centers = np.array(fit_bin_centers)
        fit_evts = np.array(fit_evts)
        fit_evts_unc = np.array(fit_evts_unc)
        if len(fit_range)>0:
            print("Pedestal TRYING FIT RANGE: " + str(fit_range))
            fit_bin_inds = np.where((bin_centers > fit_range[0]) & (bin_centers < fit_range[1]))[0]
            fit_bin_centers = fit_bin_centers[fit_bin_inds]
            fit_evts = fit_evts[fit_bin_inds]
            #fit_vts_unc = fit_evts_unc[fit_bin_inds]
            fit_evts_unc = fit_evts_unc[fit_bin_inds]#gian
        print("Pedestal TRYING INITIAL PARAMS: " + str(init_params))
        #print("TRYING BIN CENTERS: " + str(bin_centers))
        #print("EVENTS: " + str(evts))
        try:
            popt, pcov = scp.curve_fit(fu.gauss1, bin_centers, evts, p0=init_params, maxfev=6000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT TO PEDESTAL AFTER ITERATIONS...")
            popt = None
            pcov = None
            return popt, pcov, bin_centers, evts, evts_unc
        self.ped_fit_x = bin_centers
        self.ped_fit_y =fu.gauss1(self.ped_fit_x,popt[0],popt[1],popt[2])
        perr = np.diag(pcov)
        self.ped_fit_y_unc =abs(fu.gauss1(self.ped_fit_x,popt[0]+perr[0],popt[1],popt[2]+perr[2]) - 
                               fu.gauss1(self.ped_fit_x,popt[0]-perr[0],popt[1],popt[2]-perr[2]))
        self.ped_mean = popt[1]
        self.ped_sigma = popt[2]
        #self.ped_fit_y =fu.OrderStat(self.ped_fit_x,popt[0],popt[1],popt[2],popt[3]) 
        #self.ped_mean = popt[2]
        #self.ped_sigma = popt[3]
        if fit_tail is True:
            print("fitting pedestal tail")
            exp_ind = []
            if len(exp_fit_range) > 0:
                exp_ind = np.where((bin_centers > exp_fit_range[0]) & (bin_centers < exp_fit_range[1]))[0]
            else:
                exp_ind = np.where((bin_centers > self.ped_mean+self.ped_sigma) & (bin_centers < self.ped_mean + 3*self.ped_sigma))[0]
            exp_bins = bin_centers[exp_ind]
            exp_evts = evts[exp_ind]
            exp_evts_unc = evts_unc[exp_ind]
            #exp_init_params = [popt[0]/popt[2],popt[2],10*popt[1]]
            exp_init_params = [exp_evts[0],popt[2],10*popt[1]]
            print("EXPONENTIAL FIT: INIT PARAMS: " + str(exp_init_params))
            print("EXPONENTIAL x bins for the fit: " + str(exp_bins))
            print("EXPONENTIAL y bins for the fit: " + str(exp_evts))
            try:
                eopt, ecov = scp.curve_fit(lambda x,D,tau,t: fu.gaussPlusExpo(x,popt[0],popt[1],popt[2],D,tau,t), 
                        exp_bins, exp_evts, p0=exp_init_params, sigma=exp_evts_unc, maxfev=12000)
                #eopt, ecov = scp.curve_fit(lambda x,D,tau,t: D*np.exp(-(x-t)/tau), 
                #        exp_bins, exp_evts, p0=exp_init_params, maxfev=12000)
            except RuntimeError:
                print("NO SUCCESSFUL FIT TO PEDESTAL AFTER ITERATIONS...")
                popt = None
                pcov = None
                return popt, pcov, bin_centers, evts, evts_unc
            popt = np.concatenate((popt,eopt))
            #
            self.ped_fit_y =fu.gaussPlusExpo(self.ped_fit_x,popt[0],popt[1],
                    popt[2],eopt[0],eopt[1],eopt[2]) 

        #print("TRYING BIN CENTERS: " + str(bin_centers))
        print("optimal parameters after fitting to the pedestal: " + str(popt))
        return popt, pcov, bin_centers,evts,evts_unc

    def FitPEPeaks(self,HistName,exclude_ped = True, subtract_ped = False,
            fit_range = []):
        thehist =  self.ROOTFile.Get(HistName)
        #Get histogram information into ntuples
        bin_centers, evts,evts_unc =(), (), () #pandas wants ntuples
        fit_bin_centers, fit_evts,fit_evts_unc =(), (), () #pandas wants ntuples
        for i in range(int(thehist.GetNbinsX()+1)):
            if i==0:
                continue
            bin_centers =  bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            evts = evts + (thehist.GetBinContent(i),)
            evts_unc = evts_unc + (thehist.GetBinError(i),)
#            if exclude_ped is True and ((float(thehist.GetBinWidth(i))/2.0) + \
#                    float(thehist.GetBinLowEdge(i)) < (self.ped_mean + 3*self.ped_sigma)):
#                continue
            fit_bin_centers =  fit_bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            fit_evts = fit_evts + (thehist.GetBinContent(i),)
            fit_evts_unc = fit_evts_unc + (thehist.GetBinError(i),)
        bin_centers = np.array(bin_centers)
        evts = np.array(evts)
        evts_unc = np.array(evts_unc)
        fit_bin_centers = np.array(fit_bin_centers)
        fit_evts = np.array(fit_evts)
        fit_evts_unc = np.array(fit_evts_unc)
        if len(fit_range)>0:
            print("selecting range to fit PE peaks")
            fit_bin_inds = np.where((fit_bin_centers > fit_range[0]) & (fit_bin_centers < fit_range[1]))[0]
            fit_bin_centers = fit_bin_centers[fit_bin_inds]
            fit_evts = fit_evts[fit_bin_inds]
            fit_evts_unc = fit_evts_unc[fit_bin_inds]
        if subtract_ped:
            print("subtracting ped")
            fit_evts = fit_evts - self.ped_fit_y
            fit_evts_unc = np.sqrt(evts_unc**2 + self.ped_fit_y_unc**2)#why 
        if exclude_ped:
            print("excluding the ped -> ped_mean = " + str(self.ped_mean))
            print("excluding the ped -> ped_sigma = " + str(self.ped_sigma))
            print("excluding the ped -> consider bins greater/equal than (self.ped_mean + 1*self.ped_sigma) = " + str(self.ped_mean + 1*self.ped_sigma))
            #testing new range to exclude for badpmts
            #fit_bin_inds = np.where(bin_centers>=(self.ped_mean - 5*self.ped_sigma)) #PMT 353 simple Gauss fittype
            fit_bin_inds = np.where(bin_centers>=(self.ped_mean+1*self.ped_sigma)) 
            fit_evts = fit_evts[fit_bin_inds]
            fit_evts_unc = fit_evts_unc[fit_bin_inds]
            fit_bin_centers = fit_bin_centers[fit_bin_inds]
        zerobins = np.where(fit_evts_unc<=1)[0]
        fit_evts_unc[zerobins] = 1.15
        #print("bins with 1.15: " + str(zerobins))
        #print("unc in bins with 1.15: " + str(fit_evts_unc))
        #print("unc in bins with 1.15: " + str(fit_evts_unc[zerobins]))
        #plt.errorbar(fit_bin_centers,fit_evts,yerr=fit_evts_unc,marker='o',linestyle="None")
        #plt.show()
        if (subtract_ped and exclude_ped):
           print("After subtracting and excluding ped the mean of the distribution is %f"%(np.mean(fit_evts)))
        print("Fitting initial params (a new initial mean was set by the user before): " + str(self.initial_params))
        print("Fit bounds:" + str(self.lower_bounds) + "    " +str(self.upper_bounds))
        try:
            if self.lower_bounds is None or self.upper_bounds is None:
                print("inside the nobounds fit")
                popt, pcov = scp.curve_fit(self.fitfunc, fit_bin_centers, fit_evts, p0=self.initial_params, 
                        sigma = fit_evts_unc, maxfev=6000)
            else:
                print("inside the yesbounds fit")
                popt, pcov = scp.curve_fit(self.fitfunc, fit_bin_centers, fit_evts, p0=self.initial_params,
                      bounds=(self.lower_bounds,self.upper_bounds),sigma = fit_evts_unc,maxfev=8000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT AFTER ITERATIONS...")
            popt = None
            pcov = None
        return popt, pcov, bin_centers, evts, evts_unc

    def FitPEPeaksV2(self,HistName,exclude_ped = True, subtract_ped = False):
        thehist =  self.ROOTFile.Get(HistName)
        #Get histogram information into ntuples
        bin_centers, evts,evts_unc =(), (), () #pandas wants ntuples
        fit_bin_centers, fit_evts,fit_evts_unc =(), (), () #pandas wants ntuples
        for i in range(int(thehist.GetNbinsX()+1)):
            if i==0:
                False #I put this stuff
                continue
            bin_centers =  bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            evts = evts + (thehist.GetBinContent(i),)
            evts_unc = evts_unc + (thehist.GetBinError(i),)
            if exclude_ped is True and ((float(thehist.GetBinWidth(i))/2.0) + \
                    float(thehist.GetBinLowEdge(i)) < (self.ped_mean + 3*self.ped_sigma)):
                continue
            fit_bin_centers =  fit_bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            fit_evts = fit_evts + (thehist.GetBinContent(i),)
            fit_evts_unc = fit_evts_unc + (thehist.GetBinError(i),)
        bin_centers = np.array(bin_centers)
        evts = np.array(evts)
        evts_unc = np.array(evts_unc)
        fit_bin_centers = np.array(fit_bin_centers)
        fit_evts = np.array(fit_evts)
        fit_evts_unc = np.array(fit_evts_unc)
        if subtract_ped == True:
            #Subtract off the pedestal
            ped_sub_evts = copy.deepcopy(evts)
            ped_sub_evts_unc = copy.deepcopy(evts_unc)

            #Need to subtract across pedestal fit range
            ped_start_ind = np.where(bin_centers == min(self.ped_fit_x))[0]
            for i,b in enumerate(self.ped_fit_x):
                ped_sub_evts[ped_start_ind+i] = ped_sub_evts[ped_start_ind+i] - self.ped_fit_y[i]
                #FIXME: Also want to correct for uncertainty in fit
            evts = ped_sub_evts
            evts_unc = ped_sub_evts_unc

        try:
            self.initial_params.append(100000)
            newtry = lambda x,C1,m,s,Cf,f1,f2,P: fu.gauss1(P,self.ped_mean,self.ped_sigma)*fu.gauss2dep(C1,m,s,Cf,f1,f2)
            if self.lower_bounds is None or self.upper_bounds is None:
                popt, pcov = scp.curve_fit(newtry, fit_bin_centers, fit_evts, p0=self.initial_params, maxfev=6000)
            else:
                popt, pcov = scp.curve_fit(self.fitfunc, fit_bin_centers, fit_evts, p0=self.initial_params,
                      bounds=(self.lower_bounds,self.upper_bounds),maxfev=6000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT AFTER ITERATIONS...")
            popt = None
            pcov = None
        return popt, pcov, bin_centers, evts, evts_unc
