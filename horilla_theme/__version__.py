"""
Version and metadata information for the horilla_theme module.
"""

from horilla.utils.translation import gettext_lazy as _

__version__ = "1.1.0"
__module_name__ = "Theme Manager"
__release_date__ = "17 April 2026"
__description__ = _(
    "Module providing customizable color themes and UI personalization."
)
__icon__ = "horilla_theme/assets/icons/theme.svg"

__1_1_0__ = _(
    "Improved dynamic Tailwind theme integration with adoption of primary_600 "
    "for dynamic theme coloring, improved fallback handling for theme variables, "
    "and brand-aligned icon color updates across modules."
)

__1_0_0__ = _(
    "Introduced fully dynamic Theme Manager with per-company theme customization, "
    "global default theme support, dynamic Tailwind config injection, and "
    "surface color system for advanced UI backgrounds."
)
