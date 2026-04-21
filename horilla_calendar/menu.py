"""
This module registers Floating, Settings, My Settings, and Main Section menus
for the Horilla Calendar app
"""

from horilla.menu import main_section_menu, my_settings_menu, sub_section_menu

# First party / Horilla imports
from horilla.urls import reverse_lazy
from horilla.utils.translation import gettext_lazy as _
from horilla_calendar.models import GoogleIntegrationSetting
from horilla_core.menu import IntegrationsSettings

# Register Google Integration under Settings → Integrations
IntegrationsSettings.items.append(
    {
        "label": _("Google Calendar Sync"),
        "url": reverse_lazy("horilla_calendar:google_integration_settings"),
        "hx-target": "#settings-content",
        "hx-push-url": "true",
        "hx-select": "#google-integration-settings-view",
        "hx-select-oob": "#settings-sidebar",
        "perm": "horilla_calendar.change_googleintegrationsetting",
    }
)


@main_section_menu.register
class AnalyticsSection:
    """
    Registers the Schedule section in the main sidebar.
    """

    section = "schedule"
    name = _("Schedule")
    icon = "/assets/icons/schedule.svg"
    position = 4


@my_settings_menu.register
class GoogleCalendarSettings:
    """Registers Google Calendar integration in the My Settings sidebar."""

    title = _("Google Calendar")
    url = reverse_lazy("horilla_calendar:google_calendar_settings")
    active_urls = "horilla_calendar:google_calendar_settings"
    order = 5
    attrs = {
        "hx-boost": "true",
        "hx-target": "#my-settings-content",
        "hx-push-url": "true",
        "hx-select": "#google-calendar-settings-view",
        "hx-select-oob": "#my-settings-sidebar",
    }
    condition = staticmethod(GoogleIntegrationSetting.google_calendar_enabled)


@sub_section_menu.register
class CalendarSubSection:
    """
    Registers the calendar  menu to sub section in the main sidebar.
    """

    section = "schedule"
    verbose_name = _("Calendar")
    icon = "assets/icons/calendar.svg"
    url = reverse_lazy("horilla_calendar:calendar_view")
    app_label = "horilla_calendar"
    position = 1
    attrs = {
        "hx-boost": "true",
        "hx-target": "#mainContent",
        "hx-select": "#mainContent",
        "hx-swap": "outerHTML",
    }
