#############################################################################
##
##      Filename: remnant.py
##
##      Author: Tousif Islam
##
##      Created: 01-05-2023
##
##      Description: Calculates properties of the final black hole in a 
##                   BBH merger using GPR fits
##
##      Modified:
##
#############################################################################

import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
import pickle
import argparse
import sys, subprocess

import os
package_home = os.path.dirname(__file__) 

class BHPTNRSurRemnant():
    """
    Class to load GPR fits and generate remnant properties
    """
    
    def __init__(self):
        gpr_models = self._load_fits()
        self.mf_model = gpr_models['remnant_mass']
        self.sf_model = gpr_models['remnant_spin']
        self.vf_model = gpr_models['remnant_kick']
        self.Lpeak_model = gpr_models['peak_luminosity']
        
        
    def _load_fits(self):
        """
        loads pickle file containing GPR fits for the remnant mass, remnant spin,
        peak luminosity and kick velocity
        """
        models = []
        
        if os.path.isfile("%s/data/BHPTNRSur1dq1e3_remnant.pickle"%package_home)==False:
            os.system('wget https://zenodo.org/record/8162005/files/BHPTNRSur1dq1e3_remnant.pickle -P %s/data/'%(package_home))
            print('... remnant fit downloaded')
        
        with open("%s/data/BHPTNRSur1dq1e3_remnant.pickle"%package_home, "rb") as f:
            while True:
                try:
                    models.append(pickle.load(f))
                except EOFError:
                    break

        gpr_models = {'remnant_mass': models[0],
                      'remnant_spin': models[1],
                      'remnant_kick': models[2], 
                      'peak_luminosity': models[3]}

        return gpr_models


    def _X_parameterization(self, X_input):
        """
        transform input params to fit params : q to log10(q)
        """
        X_fit = np.array([np.log10(X_input)])
        return X_fit.reshape(-1,1)

    
    def _gpr_output_to_remnant_mass(self, gpr_eval):
        """
        transforms fit output to physical remnant mass
        """
        return 1-10**gpr_eval

    
    def _gpr_output_to_remnant_spin(self, gpr_eval):
        """
        transforms fit output to physical remnant spin
        """
        return 10**gpr_eval
    
    
    def _gpr_output_to_remnant_kick(self, gpr_eval):
        """
        transforms fit output to physical remnant kick velocity
        """
        return 10**gpr_eval

    
    def _gpr_output_to_peak_lumoinosity(self, gpr_eval):
        """
        transforms fit output to physical peak luminosity values
        """
        return 10**gpr_eval
    
    
    def _gpr_err_remnant_mass(self, gpr_eval, grp_err_eval):
        """
        computes the error in GPR fits in the linear scale
        """
        return self._gpr_output_to_remnant_mass(gpr_eval + grp_err_eval) - self._gpr_output_to_remnant_mass(gpr_eval)
    
    
    def _evaluate_Mf_fit_at_Xfit(self, X_fit):
        """
        evaluates GPR fits at the parameterized X values for the remnant mass
        """
        # compute GPR model predictions
        mf_gpr, mferr_gpr = self.mf_model.predict(X_fit, return_std=True)
        # transform the fit outputs to meaningful physical quantities
        mf = self._gpr_output_to_remnant_mass(mf_gpr)
        # compute GPR errors in the linear scale
        mferr = self._gpr_output_to_remnant_mass(mf_gpr + mferr_gpr) - self._gpr_output_to_remnant_mass(mf_gpr)
        return mf, mferr
    
    def _evaluate_Sf_fit_at_Xfit(self, X_fit):
        """
        evaluates GPR fits at the parameterized X values for the remnant spin
        """
        # compute GPR model predictions
        sf_gpr, sferr_gpr = self.sf_model.predict(X_fit, return_std=True)
        # transform the fit outputs to meaningful physical quantities
        sf = self._gpr_output_to_remnant_mass(sf_gpr)
        # compute GPR errors in the linear scale
        sferr = self._gpr_output_to_remnant_spin(sf_gpr + sferr_gpr) - self._gpr_output_to_remnant_spin(sf_gpr)
        return sf, sferr
    
    def _evaluate_vf_fit_at_Xfit(self, X_fit):
        """
        evaluates GPR fits at the parameterized X values for the remnant kick
        """
        # compute GPR model predictions
        vf_gpr, vferr_gpr = self.vf_model.predict(X_fit, return_std=True)
        # transform the fit outputs to meaningful physical quantities
        vf = self._gpr_output_to_remnant_kick(vf_gpr)
        # compute GPR errors in the linear scale
        vferr = self._gpr_output_to_remnant_kick(vf_gpr + vferr_gpr) - self._gpr_output_to_remnant_kick(vf_gpr)
        return vf, vferr
    
    
    def _evaluate_Lpeak_fit_at_Xfit(self, X_fit):
        """
        evaluates GPR fits at the parameterized X values for the peak luminosity
        """
        # compute GPR model predictions
        Lp_gpr, Lperr_gpr = self.Lpeak_model.predict(X_fit, return_std=True)
        # transform the fit outputs to meaningful physical quantities
        Lp = self._gpr_output_to_peak_lumoinosity(Lp_gpr)
        # compute GPR errors in the linear scale
        Lperr = self._gpr_output_to_peak_lumoinosity(Lp_gpr + Lperr_gpr) -  self._gpr_output_to_peak_lumoinosity(Lp_gpr)
        return Lp, Lperr
    
    
    def _evaluate_fit_at_Xfit(self, X_fit):
        """
        evaluates all GPR fits at the parameterized X values
        """        
        mf, mferr = self._evaluate_Mf_fit_at_Xfit(X_fit)
        sf, sferr = self._evaluate_Sf_fit_at_Xfit(X_fit)
        vf, vferr = self._evaluate_Sf_fit_at_Xfit(X_fit)
        Lp, Lperr = self._evaluate_Sf_fit_at_Xfit(X_fit) 
        return mf, mferr, sf, sferr, vf, vferr, Lp, Lperr
        
        
    def evaluate_fit(self, X_input):
        """
        evaluate all GPR fits at a given value of the BBH parameter
        """
        X_fit = self._X_parameterization(X_input)
        mf, mferr, sf, sferr, vf, vferr, Lp, Lperr = self._evaluate_fit_at_Xfit(X_fit)
        if isinstance(X_input, np.ndarray) or isinstance(X_input, list):
            return mf, mferr, sf, sferr, vf, vferr, Lp, Lperr 
        else:
            return mf[0], mferr[0], sf[0], sferr[0], vf[0], vferr[0], Lp[0], Lperr[0]