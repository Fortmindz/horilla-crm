"""
Version and metadata for the horilla_dashboard app.

Contains the module's version string and descriptive metadata used in the
application registry and UI.
"""

from horilla.utils.translation import gettext_lazy as _

__version__ = "1.5.0"
__module_name__ = "Dashboards"
__release_date__ = "17 April 2026"
__description__ = _("Module for building and customizing interactive dashboards.")
__icon__ = "assets/icons/icon6.svg"

__1_5_0__ = _(
    "Extended dashboard generator to support multiple charts, multiple table "
    "widgets, and custom KPI functions. Added more KPI widgets and improved "
    "charts and reporting components for the leads dashboard."
)

__1_4_0__ = _(
    "Added configurable Y-axis metrics for charts reusing KPI options, plus new "
    "chart types: Area, Tree Map, Heat Map, Radar, Sankey, and Scatter."
)

__1_3_0__ = _(
    "Added advanced visualization capabilities including multi-series charts, "
    "improved stacked chart rendering, interactive chart previews in dashboard "
    "editor, and enhanced analytics widgets for deeper CRM insights."
)

__1_2_0__ = _(
    "Migrated from Django AppConfig to Horilla AppLauncher and and replaced Django utilities"
    "with horilla.utils.decorators, horilla.utils.translation, and horilla.shortcuts where applicable."
)

__1_1_0__ = _(
    "Added drag and drop reordering from home page, date range filter,"
    "and set to default options for enhanced dashboard customization and data visualization."
)
