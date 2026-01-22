"""
Django admin configuration for horilla_notifications app.

This module registers the Notification model with the Django admin interface,
allowing administrators to manage notifications through the admin panel.
"""

# horilla_notifications/admin.py

# Third party imports (Django)
from django.contrib import admin

# Local application imports
from .models import Notification

admin.site.register(Notification)

# Register your notifications models here.
