#############################################################################
##
##      Filename: analytical_fits.py
##
##      Author: Tousif Islam
##
##      Created: 01-05-2023
##
##      Description: Calculates properties of the final black hole in
##                   point particle limit
##
##      Modified:
##
#############################################################################

import numpy as np

class PointParticle():
    """
    Analytical expression for the BHPT remnant properties
    
    following (i) Hofmann, Barausse and Rezzolla / https://arxiv.org/pdf/1605.01938.pdf
              (ii) Haegel and Husa / https://arxiv.org/pdf/1911.01496.pdf
    """
    def __init__(self, q, a=0):
        self.q = q
        self.a = a
        self.M = 1
        self.r_isco = self._compute_r_isco()
        self.E_at_isco = self._compute_Energy_at_isco()
        self.Erad = self._compute_Erad_isco()
        self.Lrad = self._compute_Lrad_isco()
        self.Mfinal = self._compute_Mfinal()
        self.afinal = self._compute_afinal()
        
    def _symmetric_mass_ratio(self):
        """
        compute symmetric mass ratio
        """
        return self.q/(1+self.q)**2
    
    def _Z1(self):
        """
        auxilary function for computing r_isco
        """
        return 1 + ((1-self.a*self.a)**(1/3)) * ( (1+self.a*self.a)**(1/3) + (1-self.a*self.a)**(1/3))
    
    def _Z2(self):
        """
        auxilary function for computing r_isco
        """
        Z1 = self._Z1()
        return np.sqrt(3*self.a*self.a + Z1*Z1)
    
    def _sign_of_a(self):
        """
        compute sign of the spin
        """
        if self.a<0.0:
            sign = -1
        else:
            sign = 1
        return sign
    
    def _compute_r_isco(self):
        """
        compute radius at the ISCO
        """
        Z1 = self._Z1()
        Z2 = self._Z2()
        sign = self._sign_of_a()
        return 3 + Z2 - sign * np.sqrt((3-Z1)*(3+Z1+2*Z2))
    
    def _compute_Energy_at_isco(self):
        """
        compute radiated energy at the ISCO
        """
        return np.sqrt( 1 - 2/(3*self.r_isco) )
    
    def _compute_Erad_isco(self):
        """
        compute radiated energy until the ISCO
        """
        nu = self._symmetric_mass_ratio()
        return nu * ( 1 - self.E_at_isco )
    
    def _compute_Lrad_isco(self):
        """
        compute radiated orbital angular momenta at the ISCO
        """
        nu = self._symmetric_mass_ratio()
        return (2*nu* (3*np.sqrt(self.r_isco) - 2*self.a) ) / (np.sqrt(3*self.r_isco))
    
    def _compute_Mfinal(self):
        """
        compute mass of the remnant
        """
        return 1 - self.Erad
    
    def _compute_afinal(self):
        """
        compute spin of the remnant
        """
        return (self.Lrad + self.a*self.M*self.M) / self.Mfinal**2
    
    def obtain_final_state(self):
        """
        compute mass and spin of the remnant
        """
        mf = self._compute_Mfinal()
        sf = self._compute_afinal()
        return mf, sf
    
    
        

