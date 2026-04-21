"""Admin configuration for horilla_calendar app."""

from django.contrib import admin

from .models import (
    CustomCalendar,
    CustomCalendarCondition,
    GoogleCalendarConfig,
    UserAvailability,
    UserCalendarPreference,
)

admin.site.register(UserCalendarPreference)
admin.site.register(UserAvailability)
admin.site.register(CustomCalendar)
admin.site.register(CustomCalendarCondition)
admin.site.register(GoogleCalendarConfig)
