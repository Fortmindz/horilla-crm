"""Module containing package metadata used by Horilla (version, name, icons)."""

from django.utils.translation import gettext_lazy as _

__version__ = "1.9.0"
__module_name__ = _("Core System")
__release_date__ = "17 April 2026"
__description__ = _(
    "Core system providing authentication, configuration, utilities, and platform-level services."
)
__icon__ = "assets/icons/logo.png"


__1_9_0__ = _(
    "Added Google Calendar integration with sync, service, and settings support. "
    "Implemented cadence signals for runtime activities. Centralized HorillaView "
    "layout resolution with get_layout_url() for backend-driven layout selection."
)


__1_8_1__ = _(
    "Switched Channels backend from InMemoryChannelLayer to RedisChannelLayer. "
    "Moved Holiday model to dedicated holidays.py. Improved branch list layout, "
    "business hour and holiday bulk select, and viewport-based table heights. "
    "Added SECURITY.md documentation."
)


__1_8_0__ = _(
    "Introduced unified Process Builder system combining reviews and approvals. "
    "Added async notification and mail handling with background thread execution. "
    "Improved health check endpoint and version changelog modal system. "
    "Updated assign_first_company_to_all_users signal to use User model directly."
)


__1_7_0__ = _(
    "Strengthened core validation with strict enforcement of include_models during "
    "feature registration, validation of subsection-to-section mappings, and export "
    "of StreamingHttpResponse via Horilla HTTP utilities."
)


__1_6_0__ = _(
    "Added health check endpoint, synced fiscal year and period logic, "
    "improved version changelog modal system, and switched Django Channels "
    "backend to Redis for better performance and reliability."
)


__1_5_0__ = _(
    "Improved global search model registry loading, standardized error handling "
    "with dedicated 403, 404, 405, and 500 templates, strengthened authentication "
    "flow using Django authenticate(), and applied multiple security and "
    "stability improvements across internal views."
)


__1_4_0__ = _(
    "Introduced the Horilla AppLauncher system for dynamic application "
    "registration. Added horilla.shortcuts, horilla.urls, and horilla.utils "
    "utilities. Refactored project URL handling and improved internal "
    "framework architecture for modular applications."
)


__1_2_0__ = _(
    "Improved system configuration handling, strengthened dashboard layout "
    "validation, enhanced filter processing reliability, and added multiple "
    "defensive validation improvements across core components."
)


__1_1_0__ = _(
    "Added an 'All Companies' option to the company dropdown, allowing users "
    "to view data irrespective of company selection."
)
