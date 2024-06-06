import numpy as np
import scipy.special as sps
import scipy.stats as scs
import matplotlib.pyplot as plt
#def gauss2(x,p0):
#    return p0[0]*(1./(p0[1]*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-p0[2])**2/p0[1]**2) + \
#                                    p0[3]*(1./(p0[4]*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-p0[5])**2/p0[4]**2) 
#
#
#def gauss3(x,*p0):
#    return p0[0]*(1./np.sqrt(((p0[1]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[2])**2/p0[1]**2) + \
#                                    p0[3]*(1./np.sqrt(((p0[4]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[5])**2/p0[4]**2) + \
#                                    p0[6]*(1./np.sqrt(((p0[7]**2)*2*np.pi)))*np.exp(-(1./2.)*(x-p0[8])**2/p0[7]**2)
#

def WeightedMean(x,w):
    return np.sum((w*x)/np.sum(w))

def WeightedStd(x,w):
    nonzerow = np.where(w > 0)[0]
    M = np.sum(w[nonzerow])
    WMean = WeightedMean(x,w)
    return np.sqrt(np.sum(w*((x-WMean)**2))/(((M-1)/M)*np.sum(w)))

def Poisson(x,mu):
    return (mu**x)*np.exp(-mu)/sps.gamma(x)

def OrderStat(x,A,n,mu,s):
    return gauss1(x,A,mu,s)*((1./2)*((1 + sps.erf((x-mu)/s)))**(n-1))

def OrderStatPlusExpo(x,A,n,mu,s,D,tau,t):
    return gauss1(x,A,mu,s)*((1./2)*((1 + sps.erf((x-mu)/s)))**(n-1)) + D*(np.exp(-(x-t)/tau)) 

def Gamma(x,mu,b):
    return (1./(b*mu*sps.gamma(1./b))) * (x/(b*mu))**((1./b)-1) * np.exp(-(x/(b*mu)))

Beta = lambda x,amp,A,s,y: amp*scs.beta.pdf(x,s,y)/A


#gauss1= lambda x,C1,m1,s1: C1*(1./(s1*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m1)**2)/s1**2)
gauss1= lambda x,C1,m1,s1: C1*np.exp(-(1./2.)*((x-m1)**2)/s1**2)

landau = lambda x,C,m,l1,l2: C*((1./np.sqrt(2*np.pi))*np.exp(-(1./2)*(((x-m)/l1) + np.exp(-(x-m)/l2))))

gauss2dep= lambda x,C1,m,s,Cf,f1,f2: C1*(1./(s*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m)**2)/s**2) + \
                                    C1*Cf*(1./(f2*s*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-(f1*m))**2)/(f2*s)**2)

gauss3dep= lambda x,C1,m,s,Cf,f1,f2: C1*(1./(s*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m)**2)/s**2) + \
                                    C1*Cf*(1./(f2*s*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-(f1*m))**2)/(f2*s)**2) + \
                                    C1*(Cf**2)*(1./((f2**2)*s*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-(2*f1*m))**2)/((f2**2)*s)**2)



def SPEGaussians(x,C1,mu,s,f_C,f_mu,f_s,C3,l):
   '''
   Returns the distribution related from single PE response of a PMT.  
   One gamma models the completely amplified PEs, while another is related
   to incomplete amplification ( 0 < f_mu < 1 and f_b free).
   C1: magnitude of primary gamma
   C2: magnitude of secondary gamma

   '''
   base_SPE = gauss1(x,C1,mu,s) + gauss1(x,f_C*C1,f_mu*mu,f_s*s)
   #Add exponential correction for even more incomplete amplification
   exponential_range = np.where(x<mu)[0]
   exp_x = x[exponential_range]
   exp_SPE = C3*l*np.exp(-x[exponential_range]*l)
   base_SPE[exponential_range] = base_SPE[exponential_range] + exp_SPE
   return base_SPE

def SPEGaussians_NoExp(x,C1,mu,s,f_C,f_mu,f_s):
   '''
   Returns the distribution related from single PE response of a PMT.  
   One gamma models the completely amplified PEs, while another is related
   to incomplete amplification ( 0 < f_mu < 1 and f_b free).
   C1: magnitude of primary gamma
   C2: magnitude of secondary gamma

   '''
   return gauss1(x,C1,mu,s) + gauss1(x,f_C*C1,f_mu*mu,f_s*s)

def SimpleGauss(x,C1,mu,s):
   return gauss1(x,C1,mu,s) 

def PE2Convolve(x,C1,mu,s,f_C,f_mu,f_s,S_C):
    return (S_C)*np.convolve(SPEGaussians_NoExp(x,C1,mu,s,f_C,f_mu,f_s),
                                             SPEGaussians_NoExp(x,C1,mu,s,f_C,f_mu,f_s),
                                             "same")

def EXP2SPE(x,C1,mu,s,f_C,f_mu,f_s,S_C,D,tau,f_t):#,S_mu,S_s):
    exponen = expo(x,D,tau,f_t)
    single_SPE = SPEGaussians_NoExp(x,C1,mu,s,f_C,f_mu,f_s)
    two_PE = gauss1(x,S_C*C1*(1+f_C),mu*(1+f_mu),s*np.sqrt(1+(f_s)**2)) +  \
            gauss1(x,S_C*2*C1,2*mu,s*np.sqrt(2)) # + \
            #gauss1(x,S_C*C1*2*f_C, 2*mu*f_mu,s*f_s*np.sqrt(2))
    return exponen + single_SPE + two_PE

def EXP3SPE(x,C1,mu,s,f_C,f_mu,f_s,S_C,D,tau,f_t,S_C3):#,S_mu,S_s):
    exponen = expo(x,D,tau,f_t)
    single_SPE = SPEGaussians_NoExp(x,C1,mu,s,f_C,f_mu,f_s)
    two_PE = gauss1(x,S_C*C1*(1+f_C),mu*(1+f_mu),s*np.sqrt(1+(f_s)**2)) +  \
            gauss1(x,S_C*2*C1,2*mu,s*np.sqrt(2)) # + \
            #gauss1(x,S_C*C1*2*f_C, 2*mu*f_mu,s*f_s*np.sqrt(2))
    three_PE = gauss1(x,(S_C3)*2*S_C*C1,3*mu,s*np.sqrt(3))
    return exponen + single_SPE + two_PE + three_PE

def SPE2Peaks(x,C1,mu,s,f_C,f_mu,f_s,S_C):#,S_mu,S_s):
    single_SPE = SPEGaussians_NoExp(x,C1,mu,s,f_C,f_mu,f_s)
    two_PE = gauss1(x,S_C*C1*(1+f_C),mu*(1+f_mu),s*np.sqrt(1+(f_s)**2)) +  \
            gauss1(x,S_C*2*C1,2*mu,s*np.sqrt(2)) # + \
            #gauss1(x,S_C*C1*2*f_C, 2*mu*f_mu,s*f_s*np.sqrt(2))
    return single_SPE + two_PE

def SPE3Peaks(x,C1,mu,s,f_C,f_mu,f_s,S_C1,S_C2):#,S_mu,S_s):
    single_SPE = SPEGaussians_NoExp(x,C1,mu,s,f_C,f_mu,f_s)
    two_PE = gauss1(x,S_C1*C1*(1+f_C),mu*(1+f_mu),s*np.sqrt(1+(f_s)**2)) +  \
            gauss1(x,S_C1*2*C1,2*mu,s*np.sqrt(2)) # + \
            #gauss1(x,S_C*C1*2*f_C, 2*mu*f_mu,s*f_s*np.sqrt(2))
    three_PE = gauss1(x,S_C2*3*C1,3*mu,s*np.sqrt(3)) + \
               gauss1(x,S_C2*C1*(2+f_C),mu*(2+f_mu),s*np.sqrt(2+(f_s)**2))
    return single_SPE + two_PE + three_PE

#def SPE2Peaks(x,C1,mu,s,f_C,f_mu,f_s,S_C):#,S_mu,S_s):
#    single_SPE = SPEGaussians_NoExp(x,C1,mu,s,f_C,f_mu,f_s)
#    return single_SPE + PE2Convolve(x,C1,mu,s,f_C,f_mu,f_s,S_C)

#def SPE(x,C1,mu,b,f_C,f_mu,f_b,C3,l):
#   '''
#   Returns the distribution related from single PE response of a PMT.  
#   One gamma models the completely amplified PEs, while another is related
#   to incomplete amplification ( 0 < f_mu < 1 and f_b free).
#   C1: magnitude of primary gamma
#   C2: magnitude of secondary gamma
#
#   '''
#   base_SPE = SPE_NoExp(x,C1,mu,b,f_C,f_mu,f_b)
#   #Add exponential correction for even more incomplete amplification
#   exponential_range = np.where(x<mu )[0]
#   exp_x = x[exponential_range]
#   exp_SPE = C3*l*np.exp(-x[exponential_range]*l)
#   base_SPE[exponential_range] = base_SPE[exponential_range] + exp_SPE
#   return base_SPE
#
#def SPE_NoExp(x,C1,mu,b,f_C,f_mu,f_b):
#   '''
#   Returns the distribution related from single PE response of a PMT.  
#   One gamma models the completely amplified PEs, while another is related
#   to incomplete amplification ( 0 < f_mu < 1 and f_b free).
#   C1: magnitude of primary gamma
#   C2: magnitude of secondary gamma
#
#   '''
#   return C1*(Gamma(x,mu,b) + f_C*Gamma(x,f_mu*mu,f_b*b))
#
#def SPE2Peaks(x,C1,mu,b,f_C,f_mu,f_b,C3,l,S_C,S_mu,S_b):
#    single_SPE = SPE(x,C1,mu,b,f_C,f_mu,f_b,C3,l)
#    two_SPE = SPE_NoExp(x,S_C*C1,S_mu*mu,S_b*b,S_C*f_C,f_mu,f_b)
#    return single_SPE + two_SPE


#gauss1skew= lambda x,C1,m1,s1,a: C1*(1./(s1*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m1)**2)/s1**2)*(1 + (erf(a*(x-m1))/np.sqrt(2)))
#
#
def gaussPlusExpo(x,C1,m1,s1,D,tau,t):
    return D*(np.exp(-(x-t)/tau)) + C1*np.exp(-(1./2.)*((x-m1)**2)/s1**2)

expo = lambda x,D,tau,t: D*(np.exp(-(x-t)/tau))

#gauss2= lambda x,C1,m1,s1,C2,m2,s2: C1*(1./(s1*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m1)**2)/s1**2) + \
#                                    C2*(1./(s2*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*((x-m2)**2)/s2**2)
#
#gauss2InitialParams = np.array([300,0.001,0.0001,100,0.002,0.0005])
#
#gauss3= lambda x,C1,m1,s1,C2,m2,s2,C3,m3,s3: C1*(1./(s1*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-m1)**2/s1**2) + \
#                                    C2*(1./(s2*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-m2)**2/s2**2) + \
#                                    C3*(1./(s3*np.sqrt(2*np.pi)))*np.exp(-(1./2.)*(x-m3)**2/s3**2)
#
#gauss3InitialParams = np.array([10000,0.00001,0.0001,100,0.0005,0.002,10,0.003,0.003])
#gauss3LB = [0, 0, 0, 0, 0.0001, 0, 0, 0, 0.0005]
#gauss3UB = [1E6, 0.001, 0.0005, 1E4, 0.006, 0.01, 1E3, 0.01, 0.05]
#
#
#
gauss4= lambda x,C1,m1,s1,C2,m2,s2,C3,m3,s3,C4,m4,s4: C1*(1./(s1*np.sqrt((2*np.pi))))*np.exp(-(1./2.)*(x-m1)**2/s1**2) + \
                                    C2*(1./(s2*np.sqrt((2*np.pi))))*np.exp(-(1./2.)*(x-m2)**2/s2**2) + \
                                    C3*(1./(s3*np.sqrt((2*np.pi))))*np.exp(-(1./2.)*(x-m3)**2/s3**2) + \
                                    C4*(1./(s4*np.sqrt((2*np.pi))))*np.exp(-(1./2.)*(x-m4)**2/s4**2)

gauss4InitialParams = np.array([1000,450,6,1000,578,6,1000,750,6,1000,867,5])

