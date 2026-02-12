"""
This module registers Floating, Settings, My Settings, and Main Section menus
for the horilla_automations app
"""

from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from horilla.menu import settings_menu

# Define your menu registration logic here


@settings_menu.register
class AutomationSettings:
    """Settings menu entries for the automation module."""

    title = _("Automations")
    icon = "/assets/icons/automation.svg"
    order = 4
    items = [
        {
            "label": _("Mail & Notifications"),
            "url": reverse_lazy("horilla_automations:automation_view"),
            "hx-target": "#settings-content",
            "hx-push-url": "true",
            "hx-select": "#automation-view",
            "hx-select-oob": "#settings-sidebar",
            "perm": "horilla_automation.view_horillaautomation",
        },
    ]
