"""
This module registers Floating, Settings, My Settings, and Main Section menus
for the cadences app
"""

from horilla.menu import (
    floating_menu,
    main_section_menu,
    my_settings_menu,
    settings_menu,
    sub_section_menu,
)
from horilla.urls import reverse_lazy
from horilla.utils.translation import gettext_lazy as _
from horilla_automations.menu import AutomationSettings

# Define your menu registration logic here

automation = AutomationSettings
automation.items.extend(
    [
        {
            "label": _("Cadences"),
            "url": reverse_lazy("cadences:cadence_view"),
            "hx-target": "#settings-content",
            "hx-push-url": "true",
            "hx-select": "#cadence-view",
            "hx-select-oob": "#settings-sidebar",
            "perm": "cadences.view_cadence",
            "order": 2,
        },
    ]
)
