from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("BHPTNRremnant")
except PackageNotFoundError:
    __version__ = "unknown"

from .remnant import BHPTNRSurRemnant
from .analytical_fits import BHPTAnalyticalFits
from .point_particle import PointParticle
