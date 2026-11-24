"""Automated Architecture Scoper — deterministic SOW generator (portfolio demo)."""

__version__ = "1.0.0"

from scoper.detect import ScopeProfile, build_profile
from scoper.engine import StatementOfWork, generate_sow
from scoper.render import render_markdown
from scoper.samples import SAMPLES, get_sample

__all__ = [
    "SAMPLES",
    "ScopeProfile",
    "StatementOfWork",
    "build_profile",
    "generate_sow",
    "get_sample",
    "render_markdown",
    "__version__",
]
