import numpy as np
import scipy as sp
import lib.Functions as fu
import copy
import scipy.optimize as scp

#Class that estimates the SPE charge using a model-independent calculation
# from arXiv:1602.03150v1.  Generally you need background data (LEDs off) for 
#Each voltage setpoint to use this approach.  Instead, we will estimate the
#No-PE flashes using a fit to the pedestal and assume we can neglect dark 
#Noise. to
#ANNIE PMT Charge distributions

class FermiFitter(object):
    def __init__(self):
        print("INITIALIZING FERMIFITTER CLASS")

        self.BkgPed = {}
        self.SPEPed = {}

    def ProcessHistogram(self,rootfile,HistName):
        '''For the loaded ROOTFile, Returns a single ROOT histogram's bin data in
        a dictionary (keys are 'bins', 'bin_heights', and 'bin_height_uncs')..

        Input:
            HistName [string]
            Name of histogram to process into numpy arrays

        Output:
            hist_data [dictionary]
            Dictionary with histogram information
        '''
        thehist =  rootfile.Get(HistName)
        #Get histogram information into ntuples
        bin_centers, evts,evts_unc =(), (), () #pandas wants ntuples
        fit_bin_centers, fit_evts,fit_evts_unc =(), (), () #pandas wants ntuples
        ped_indices = []
        for i in range(int(thehist.GetNbinsX()+1)):
            #if i==0:
            #    continue
            bin_centers =  bin_centers + ((float(thehist.GetBinWidth(i))/2.0) + float(thehist.GetBinLowEdge(i)),)
            evts = evts + (thehist.GetBinContent(i),)
            evts_unc = evts_unc + (thehist.GetBinError(i),)
        bin_centers = np.array(bin_centers)
        evts = np.array(evts)
        evts_unc = np.array(evts_unc)
        hist_data = {'bins': bin_centers, 'bin_heights': evts,
                'bin_height_uncs':evts_unc}

        return hist_data

    def _EstimatePedestalBins(self,bkg_hist_data,TotalToBackgroundPedRatio):
        '''Estimates the total number of zero-PE triggers in the SPE data by
        scaling the background data by the relative pedestal heights.
        '''
        scaled_hist_data = bkg_hist_data['bin_heights']*TotalToBackgroundPedRatio
        return scaled_hist_data 

    def _EstimateOccupancy(self,total_hist_data,bkg_hist_data,charge_cut):
        '''Estimates the occupancy of the PMT.  Occupancy is defined as the
        number of triggers with at least one PE.  Estimation of the pedestal 
        (0 PE events) is done as follows:
        1 - occupancy = sum(bins up to the pedestal mean) + sum(best fit
        to pedestal and pedestal tail beyond the mean)
        '''
        A_s_ind = np.where(total_hist_data["bins"]<charge_cut)[0]
        A_b_ind = np.where(bkg_hist_data["bins"]<charge_cut)[0]
        #Need to correct for different run lengths in background run and signal run
        scale_factor = np.sum(total_hist_data["bin_heights"])/np.sum(bkg_hist_data["bin_heights"])
        A_b = np.sum(bkg_hist_data["bin_heights"][A_b_ind]*scale_factor)
        A_s = np.sum(total_hist_data["bin_heights"][A_s_ind])
        N = np.sum(total_hist_data["bin_heights"])
        zerope_estimate = (A_s*N)/(A_b)
        total_triggers = np.sum(total_hist_data['bin_heights'])
        return -np.log((zerope_estimate/total_triggers))


    def EstimateSPEMean(self,total_hist_data,bkg_hist_data,ped_cutoff):
        mean_total = fu.WeightedMean(total_hist_data['bins'],total_hist_data['bin_heights'])
        mean_pedestal = fu.WeightedMean(bkg_hist_data['bins'],bkg_hist_data['bin_heights'])
        occ = self._EstimateOccupancy(total_hist_data,bkg_hist_data,ped_cutoff)
        mean_photon_distribution = occ
        return ((mean_total - mean_pedestal)/mean_photon_distribution)
    
    def EstimateSPEVariance(self,total_hist_data,bkg_hist_data,ped_cutoff):
        var_total = fu.WeightedStd(total_hist_data['bins'],total_hist_data['bin_heights'])
        print("TOTAL VARIANCE: " + str(var_total))
        var_pedestal = fu.WeightedStd(bkg_hist_data['bins'],bkg_hist_data['bin_heights'])
        occ = self._EstimateOccupancy(total_hist_data,bkg_hist_data,ped_cutoff)
        SPEMean = self.EstimateSPEMean(total_hist_data,bkg_hist_data,ped_cutoff)
        variance_photon_distribution = occ
        mean_photon_distribution = occ
        numerator = var_total - var_pedestal - ((SPEMean**2) * variance_photon_distribution)
        return (numerator/mean_photon_distribution)

    def EstimateSPEError(self,total_hist_data,bkg_hist_data,ped_cutoff):
        '''Approximation on the variance of the SPE mean due to statistical 
        uncertainties.  This is Equation 21 in the original paper
        '''
        #Calculate the releavant variables for the equation
        occ = self._EstimateOccupancy(total_hist_data,bkg_hist_data,ped_cutoff)
        SPEMean = self.EstimateSPEMean(total_hist_data,bkg_hist_data,ped_cutoff)
        SPEVar = self.EstimateSPEVariance(total_hist_data,bkg_hist_data,ped_cutoff)
        BKGVar = fu.WeightedStd(bkg_hist_data['bins'],bkg_hist_data['bin_heights'])
        N = np.sum(total_hist_data["bin_heights"])
        #Need to correct for different run lengths in background run and signal run
        scale_factor = np.sum(total_hist_data["bin_heights"])/np.sum(bkg_hist_data["bin_heights"])
        A_b_ind = np.where(bkg_hist_data["bins"]<ped_cutoff)[0]
        A_b = np.sum(bkg_hist_data["bin_heights"][A_b_ind]*scale_factor)
        f = A_b / N  #FIXME: I'm assuming A_b / N's true distribution is gaussian so the values the mean...
        term1 = occ*(SPEMean**2 + SPEVar + 2*BKGVar)/(N*(occ**2))
        term2 =((SPEMean**2) * (np.exp(occ) + 1 - 2*f))/(f*N*(occ**2))
        return term1 + term2


#Not used, but I'm keeping in case a use comes up later for it
    def FitPedestal(self,hist_data,init_params,fit_range):
        '''
        Uses a Gaussian from the Functions library to attempt to fit
        the pedestal peak of the distribution.  A fit range can be
        given if helping down-select to the pedestal-dominant region.

        Inputs:

        hist_data [dict]
            Ouput dictionary from the ProcessHistogram method.

        init_params [array]
            Initial parameters to try fitting a single gaussian with.
            Format is [amplitude,mean,sigma].

        fit_range [array]
            Range of values to perform fit across.  Helps to down-select
            to the ped-only range.
        '''
        ped_fit = {"x": [], "y": [], "y_unc":[],"popt":[],
                "pcov":[]}

        print("FITTING TO PEDESTAL NOW")
        bin_centers = hist_data["bins"]
        evts = hist_data["bin_heights"]
        evts_unc = hist_data["bin_height_uncs"]
        fit_bin_centers = copy.deepcopy(bin_centers)
        fit_evts = copy.deepcopy(evts)
        fit_evts_unc = copy.deepcopy(evts_unc)
        if len(fit_range)>0:
            fit_bin_inds = np.where((bin_centers > fit_range[0]) & (bin_centers < fit_range[1]))[0]
            fit_bin_centers = fit_bin_centers[fit_bin_inds]
            fit_evts = fit_evts[fit_bin_inds]
            fit_vts_unc = fit_evts_unc[fit_bin_inds]
        print("TRYING INITIAL PARAMS: " + str(init_params))
        try:
            popt, pcov = scp.curve_fit(fu.gauss1, bin_centers, evts, p0=init_params, maxfev=6000)
        except RuntimeError:
            print("NO SUCCESSFUL FIT TO PEDESTAL AFTER ITERATIONS...")
            popt = None
            pcov = None
            return popt, pcov, bin_centers, evts, evts_unc
        ped_fit["x"] = bin_centers
        ped_fit["y"] = fu.gauss1(ped_fit["x"],popt[0],popt[1],popt[2])
        perr = np.diag(pcov)
        ped_fit["y_unc"] =abs(fu.gauss1(ped_fit["x"],popt[0]+perr[0],popt[1],popt[2]+perr[2]) - 
                               fu.gauss1(ped_fit["x"],popt[0]-perr[0],popt[1],popt[2]-perr[2]))
        ped_fit["popt"] = popt
        ped_fit["pcov"] = pcov
        return ped_fit

    #def _EstimateOccupancy_Old(self,total_hist_data,bkg_hist_data,TotalToBkgPedRatio):
    #    '''Estimates the occupancy of the PMT.  Occupancy is defined as the
    #    number of triggers with at least one PE.  Estimation of the pedestal 
    #    (0 PE events) is done as follows:
    #    1 - occupancy = sum(bins up to the pedestal mean) + sum(best fit
    #    to pedestal and pedestal tail beyond the mean)
    #    '''
    #    pedestal_estimate = np.sum(self._EstimatePedestalBins(bkg_hist_data,TotalToBkgPedRatio))
    #    total_triggers = np.sum(total_hist_data['bin_heights'])
    #    return -np.log((pedestal_estimate/total_triggers))
