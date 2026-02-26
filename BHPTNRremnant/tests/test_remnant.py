import numpy as np
import pytest

from BHPTNRremnant.remnant import BHPTNRSurRemnant
from BHPTNRremnant.analytical_fits import BHPTAnalyticalFits
from BHPTNRremnant.point_particle import PointParticle


class TestBHPTNRSurRemnant:
    """Tests for the GPR surrogate remnant model."""

    @pytest.fixture(scope="class")
    def model(self):
        return BHPTNRSurRemnant()

    def test_model_loads(self, model):
        assert model.mf_model is not None
        assert model.sf_model is not None
        assert model.vf_model is not None
        assert model.Lpeak_model is not None

    def test_evaluate_fit_scalar(self, model):
        mf, mferr, sf, sferr, vf, vferr, Lp, Lperr = model.evaluate_fit(10.0)
        # All outputs should be scalar floats
        for val in [mf, mferr, sf, sferr, vf, vferr, Lp, Lperr]:
            assert np.isscalar(val) or val.ndim == 0

    def test_evaluate_fit_array(self, model):
        q_values = np.array([10.0, 50.0, 100.0])
        mf, mferr, sf, sferr, vf, vferr, Lp, Lperr = model.evaluate_fit(q_values)
        for val in [mf, mferr, sf, sferr, vf, vferr, Lp, Lperr]:
            assert len(val) == 3

    def test_remnant_mass_physical(self, model):
        mf, mferr, sf, sferr, vf, vferr, Lp, Lperr = model.evaluate_fit(10.0)
        # Remnant mass should be less than total mass (1) and positive
        assert 0 < mf < 1
        # Remnant spin should be positive and less than 1
        assert 0 < sf < 1
        # Kick and luminosity should be positive
        assert vf > 0
        assert Lp > 0


class TestBHPTAnalyticalFits:
    """Tests for the analytical kick fits."""

    def test_skh_kick_fit(self):
        fit = BHPTAnalyticalFits(q=10, a=0)
        vk = fit.SKH_kick_fit()
        assert vk > 0
        # Should scale as 1/q^2
        fit2 = BHPTAnalyticalFits(q=20, a=0)
        vk2 = fit2.SKH_kick_fit()
        assert pytest.approx(vk / vk2, rel=1e-10) == 4.0

    def test_skh_corrected(self):
        fit = BHPTAnalyticalFits(q=10, a=0)
        vk_corr = fit.SKH_kick_fit_small_q_corrected()
        vk = fit.SKH_kick_fit()
        # Corrected value should be smaller (correction factor < 1 for finite q)
        assert vk_corr < vk

    def test_ifk_kick_fit(self):
        fit = BHPTAnalyticalFits(q=10, a=0)
        vk = fit.IFK_kick_fit()
        assert pytest.approx(vk, rel=1e-10) == 0.034 / 100.0


class TestPointParticle:
    """Tests for the point particle limit calculations."""

    def test_isco_schwarzschild(self):
        # For a=0 (Schwarzschild), r_isco = 6M
        pp = PointParticle(q=1000, a=0)
        assert pytest.approx(pp.r_isco, rel=1e-10) == 6.0

    def test_energy_at_isco_schwarzschild(self):
        # E_isco = sqrt(8/9) for Schwarzschild
        pp = PointParticle(q=1000, a=0)
        assert pytest.approx(pp.E_at_isco, rel=1e-10) == np.sqrt(8.0 / 9.0)

    def test_remnant_mass_less_than_total(self):
        pp = PointParticle(q=100, a=0)
        mf, sf = pp.obtain_final_state()
        assert 0 < mf < 1
        assert sf > 0

    def test_prograde_spin_smaller_isco(self):
        pp_zero = PointParticle(q=1000, a=0)
        pp_pro = PointParticle(q=1000, a=0.9)
        # Prograde spin should give smaller ISCO
        assert pp_pro.r_isco < pp_zero.r_isco
