"""Version information for the horilla_mail module."""

from horilla.utils.translation import gettext_lazy as _

__version__ = "1.1.2"
__module_name__ = "Mail"
__release_date__ = "17 April 2026"
__description__ = _(
    "Module for managing incoming and outgoing emails through mail servers and Outlook."
)
__icon__ = "assets/icons/icon1.svg"

__1_1_2__ = _(
    "Improved mail template standardization, async mail handling with "
    "background thread execution, and enhanced notification and mail "
    "action separation for approval workflows."
)

__1_1_1__ = _(
    "Minor compatibility improvements and internal stability updates "
    "to align with the enhanced generics framework and visualization system."
)
__1_1_0__ = _(
    "Migrated from Django AppConfig to Horilla AppLauncher and and replaced"
    "Django utilities with horilla.utils.decorators, horilla.utils.translation, and horilla.shortcuts where applicable."
)
