"""Version information for the horilla_duplicates module."""

from horilla.utils.translation import gettext_lazy as _

__version__ = "1.1.0"
__module_name__ = "Duplicate Control"
__release_date__ = "17 April 2026"
__description__ = _(
    "Module for detecting potential duplicate records and supporting merge workflows."
)
__icon__ = "assets/icons/clone.svg"

__1_1_0__ = _(
    "Renamed Clone Management to Duplicate Control. Added duplicate validation "
    "for inline field edits with warning modal for duplicate conflicts. "
    "Fixed duplicate detail tab injection issue and improved merge flow "
    "handling for edge cases."
)

__1_0_0__ = _(
    "Introduced duplicate management capabilities with matching rules, potential duplicate "
    "detection, and merge comparison and summary workflows."
)
