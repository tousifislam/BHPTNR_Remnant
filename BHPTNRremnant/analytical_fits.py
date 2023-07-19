#############################################################################
##
##      Filename: analytical_fits.py
##
##      Author: Tousif Islam
##
##      Created: 01-05-2023
##
##      Description: Calculates kick velocity of the final black hole in a 
##                   BBH merger using analytical fit
##
##      Modified:
##
#############################################################################

import numpy as np

class BHPTAnalyticalFits():
    """
    Analytical fits for BHPT remnant properties
    """
    def __init__(self, q, a=0):
        self.q = q
        self.a = a
        
    def SKH_kick_fit(self):
        """
        Analytical fit for the kick velocity
        Eq(5.5) and Eq(5.7) of Sundararajan, Khanna & Hughes
        https://arxiv.org/pdf/1003.0485.pdf
        """
        return (0.0440 - 0.0099*self.a - 0.0114*self.a**2 - 0.0312*self.a**3) * (1/self.q**2)
    
    def SKH_kick_fit_small_q_corrected(self):
        """
        Analytical fit for the kick velocity - corrected for small mass ratio binaries;
        Eq(5.7) of Sundararajan, Khanna & Hughes;
        Corrected using Eq(5.1)
        https://arxiv.org/pdf/1003.0485.pdf
        """
        SKH_fit = self.SKH_kick_fit()
        small_q_corr = (1-4/self.q)**0.5
        return SKH_fit * small_q_corr

    def IFK_kick_fit(self):
        """
        Analytical fit for the kick velocity - fitted to BHPTNRSur1dq1e4 estimates
        Eq(28) of Islam, Field & Khanna
        """
        return 0.034 * (1/self.q**2)

