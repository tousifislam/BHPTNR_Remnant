#############################################################################
##
##      Filename: bhptnrsur_remnant.py
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

# find the git home directory
git_home = subprocess.check_output(['git', 'rev-parse', \
    '--show-toplevel']).decode('utf-8').strip('\n')
sys.path.append('%s'%git_home)

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
        with open("%s/data/BHPTNRSur1dq1e3_remnant.pickle"%git_home, "rb") as f:
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
    
    
    def _evaluate_fit_at_Xfit(self, X_fit):
        """
        evaluates GPR fits at the parameterized X values
        """
        # compute GPR model predictions
        mf_gpr, mferr_gpr = self.mf_model.predict(X_fit, return_std=True)
        sf_gpr, sferr_gpr = self.sf_model.predict(X_fit, return_std=True)
        vf_gpr, vferr_gpr = self.vf_model.predict(X_fit, return_std=True)
        Lp_gpr, Lperr_gpr = self.Lpeak_model.predict(X_fit, return_std=True)
        
        # transform the fit outputs to meaningful physical quantities
        mf = self._gpr_output_to_remnant_mass(mf_gpr)
        sf = self._gpr_output_to_remnant_mass(sf_gpr)
        vf = self._gpr_output_to_remnant_kick(vf_gpr)
        Lp = self._gpr_output_to_peak_lumoinosity(Lp_gpr)
        
        # compute GPR errors in the linear scale
        mferr = self._gpr_output_to_remnant_mass(mf_gpr + mferr_gpr) - self._gpr_output_to_remnant_mass(mf_gpr)
        sferr = self._gpr_output_to_remnant_mass(sf_gpr + sferr_gpr) - self._gpr_output_to_remnant_mass(sf_gpr)
        vferr = self._gpr_output_to_remnant_kick(vf_gpr + vferr_gpr) - self._gpr_output_to_remnant_kick(vf_gpr)
        Lperr = self._gpr_output_to_peak_lumoinosity(Lp_gpr + Lperr_gpr) -  self._gpr_output_to_peak_lumoinosity(Lp_gpr)
        
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