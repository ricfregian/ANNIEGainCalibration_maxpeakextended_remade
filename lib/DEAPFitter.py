import numpy as np
import scipy as sp
import Functions as fu

#Class that fits the DEAP-3600 PMT charge distribution to
#ANNIE PMT Charge distributions

class DEAPFitter(object):
     def __init__(self):
         print("INITIALIZING DEAPFITTER FUNCTION")
         self.initial_params = []
         self.nPE = 2
 
     def SetNumPEPeaks(self,nPE):
         '''
         Set the number of PE peaks to try and fit to distribution
         '''
         self.nPE = nPE


     def _SPE(self,x,C1,mu,b,C2,f_mu,f_b,C3,l,mu_p):
        '''
        Returns the distribution related from single PE response of a PMT.  
        One gamma models the completely amplified PEs, while another is related
        to incomplete amplification ( 0 < f_mu < 1 and f_b free).
        C1: magnitude of primary gamma
        C2: magnitude of secondary gamma

        '''
        base_SPE = C1*fu.Gamma(x,mu,b) + C2*fu.Gamma(x,f_mu*mu,f_b*b)
        #Add exponential correction for even more incomplete amplification
        exponential_range = np.where((x<mu) & (x>mu_ped))[0]
        exp_x = x[exponential_range]
        exp_SPE = C3*l*np.exp(-x[exponential_range]*l)
        SPE[exponential_range] = base_SPE[exponential_range] + exp_SPE
        return SPE
 
    def _Ped(self,x,mu_p,s_p):
        return fu.Gauss1(x,mu_p,s_p)
 
    def _DEAPFunction(x,B,A,mu_p,s_p,C1,mu,b,C2,f_mu,f_b,C3,l,mppf):
        '''
        Full function as described in arXiv article: 1705.10183
        '''
        df = A*self.Ped(x,mu_p,s_p)
        for n in range(self.nPE):
            nPE_convolution = None
            #Calculate contribution for the nth PE peak
            for n in range(self.nPE):
                if n == 0:
                    nPE_convolution = self._SPE(x,C1,mu,b,C2,f_mu,f_b,C3,l,mu_p)
                else:
                    nPE_convolution = np.convolve(nPE_convolution,
                                                  self._SPE(x,C1,mu,b,C2,
                                                            f_mu,f_b,C3,l),
                                                 "same")
            nPE_convolution = sts.poisson.pmf(1,mppf)*
                              np.convolve(nPE_convolution,self.Ped(x,mu_p,s_p),
                                          "same")
            df += nPE_convolution 
        return df
