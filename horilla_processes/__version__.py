"""
Version information for the Process Builder
"""

# First party imports (Horilla)
from horilla.utils.translation import gettext_lazy as _

__version__ = "1.1.0"
__module_name__ = "Process Builder"
__release_date__ = "17 April 2026"
__description__ = _(
    "Module for managing the process, including approval processes and review processes."
)
__icon__ = "assets/icons/process-management.svg"

__1_1_0__ = _(
    "Enhanced approval workflow with delete support in approval history, "
    "standard HTMX modal delete flow, and inline edit enforcement for "
    "pending/rejected records. Improved approval signals cleanup, "
    "review process table viewport handling, and redirect behavior."
)

__1_0_0__ = _(
    "Introduced unified Process Builder combining reviews and approvals "
    "into a flexible, condition-driven workflow engine with configurable "
    "approvers, field-level controls, and per-app process configuration."
)
