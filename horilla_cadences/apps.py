"""
App configuration for the cadences app.
"""

from horilla.apps import AppLauncher
from horilla.utils.translation import gettext_lazy as _


class CadencesConfig(AppLauncher):
    """
    Configuration class for the cadences app in Horilla.
    """

    default = True

    default_auto_field = "django.db.models.BigAutoField"
    name = "horilla_cadences"
    verbose_name = _("Cadences")

    url_prefix = "cadences/"
    url_module = "horilla_cadences.urls"
    url_namespace = "cadences"

    auto_import_modules = [
        "registration",
        "signals",
        "menu",
    ]
