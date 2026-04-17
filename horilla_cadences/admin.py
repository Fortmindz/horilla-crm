"""
Admin registration for the cadences app
"""

from django.contrib import admin

from .models import Cadence, CadenceFollowUp

admin.site.register(Cadence)
admin.site.register(CadenceFollowUp)

# Register your cadences models here.
