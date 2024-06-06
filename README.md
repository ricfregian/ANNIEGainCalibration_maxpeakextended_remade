Simple python fitter for PMT distributions exposed to levels of light where
they predominantly see one photon per acquisition.


##### FITTING PROCEDURE #####
First, fit the pedestal so we can exclued it from the PE peak region.
Fits keep failing to the PE region trying to fit to the pedestal, which has 
most of the statistics.  

Now, fit the two Gaussian distribution.  We can add some constraints to the
second gaussian under the model that hits are dominantly from an LED:

  - The peak should be lower than the SPE peak
  - The mean should be somewhere near twice the mean of the SPE peak
  - The sigma should be at least the same, or wider, than the SPE peak sigma

We should be able to also add in a 3 PE peak; it'll be tricker though.  It 
has to be constrained to be lower than the 2PE peak, and then the 
sigma should be wider than the 2PE peak sigma.

######Command line to run the script
python3 main.py --append ../gains_data/LED_5runs_maxpeak_winextended_remade/LEDRuns_maxpeak_fixed_Run-1.root
