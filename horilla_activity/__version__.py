"""Version information for the horilla_activity module."""

from horilla.utils.translation import gettext_lazy as _

__version__ = "1.2.1"
__module_name__ = "Activity"
__release_date__ = "17 April 2026"
__description__ = _(
    "Module for tracking and managing activities such as tasks,calls, events, and emails."
)
__icon__ = "horilla_activity/assets/icons/activity-red.svg"

__1_2_1__ = _(
    "Reduced redundant history entries, improved Many-to-Many field representation, "
    "and added cleaner labels for mail events and activity creation with "
    "new template filters for better rendering."
)

__1_2_0__ = _(
    "Improved activity workflow behavior. The Pending tab now shows all incomplete activities"
    "regardless of status label, and activity type configuration handling was enhanced "
    "for improved workflow accuracy."
)


__1_1_0__ = _(
    "Migrated from Django AppConfig to Horilla AppLauncher and replaced Django utilities with"
    "horilla.utils.decorators, horilla.utils.translation, and horilla.shortcuts where applicable."
)
