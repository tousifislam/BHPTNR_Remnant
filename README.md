# BHPTNR_Remnant

```BHPTNR_Remnant``` is an easy-to-use python package to efficiently predict the remnant mass, remnant spin, peak luminosity and the final kick imparted on the remnant black hole directly from the gravitational radiation using GPR fits. These fits have been built on the remnant data calculated from numerical relativity informed black hole perturbation theory based waveforms. 

## Tutorials

Example usage is provided in ```tutorial.ipynb``` notebook.

### Using pip
To install : ```pip install BHPTNRremnant```

A web-based example jupyter notebook tutorial is hosted here : ```https://github.com/tousifislam/BHPTNR_Remnant/blob/main/tutorials/tutorial.ipynb```
Once installed, import is as ```import BHPTNRremnant```

NR informed ppBHPT based surrogate fits can then be used as
```
# import surrogate fits
from BHPTNRremnant.remnant import BHPTNRSurRemnant

# instantiate the class
fits = BHPTNRSurRemnant()
# evaluate the fits at mass ratio q
# final mass, final spin, kick velocity and luminosity distance and their associated GPR fit error
mf, mferr, sf, sferr, vf, vferr, Lp, Lperr = fits.evaluate_fit(15)
print(mf,sf, vf,Lp)
```

One can also use the analytical fits for the kick velocities as following:
```
from BHPTNRremnant.analytical_fits import BHPTAnalyticalFits

# instantiate analytical fits
fit_obj = BHPTAnalyticalFits(q=15, a=0)
# evaluate kick velocity form Sundararajan, Khanna & Hughes
vf = fit_obj.SKH_kick_fit()
print(vf)
# evaluate kick velocity form Sundararajan, Khanna & Hughes
# corrected for the small mass ratio
vf = fit_obj.SKH_kick_fit_small_q_corrected()
print(vf)
# evaluate kick velocity form Islam, Field & Khanna
vf = fit_obj.IFK_kick_fit()
print(vf)
```

It is also possible to obtain analytical results at extreme mass ratio limit:
```
from BHPTNRremnant.point_particle import PointParticle

# instantiate point particle limit results
pp = PointParticle(q=1000, a=0)
# obtain final mass and final spin
pp.obtain_final_state()
```

## Citation guideline

If you make use of any module from the Toolkit in your research please acknowledge using:

> This work makes use of the Black Hole Perturbation Toolkit.

If you make use of the BHPTNRSur models please cite the following paper:

```
@article{Islam:2022laz,
    author = "Islam, Tousif and Field, Scott E. and Khanna, Gaurav.",
    title = "{Remnant black hole properties from numerical-relativity-informed perturbation theory and implications for waveform modelling}",
    eprint = "https://arxiv.org/abs/2301.07215",
    archivePrefix = "arXiv",
    primaryClass = "gr-qc",
    month = "1",
    year = "2023"
}
```
