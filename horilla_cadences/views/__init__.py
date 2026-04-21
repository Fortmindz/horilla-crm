"""Aggregate view modules for the `horilla_cadences.views` package."""

from horilla_cadences.views.core import (
    CadenceView,
    CadenceNavbar,
    CadenceListView,
    CadenceFormView,
    CadenceToggleView,
    CadenceDeleteView,
)
from horilla_cadences.views.followups import (
    CadenceFollowUpCreateView,
    CadenceFollowUpDeleteView,
    CadenceFollowupDoThisValueFieldView,
)
from horilla_cadences.views.detail import CadenceDetailView
from horilla_cadences.views.record_tab import CadenceRecordTabView

from horilla_cadences.views.cadence_report import (
    CadenceReportView,
    CadenceReportTabView,
    CadenceTaskTabView,
    CadenceTaskListView,
    CadenceCallTabView,
    CadenceCallListView,
    CadenceEmailTabView,
    CadenceEmailListView,
)

__all__ = [
    "CadenceView",
    "CadenceNavbar",
    "CadenceListView",
    "CadenceFormView",
    "CadenceFollowUpCreateView",
    "CadenceFollowUpDeleteView",
    "CadenceFollowupDoThisValueFieldView",
    "CadenceToggleView",
    "CadenceDeleteView",
    "CadenceDetailView",
    "CadenceRecordTabView",
    "CadenceReportView",
    "CadenceReportTabView",
    "CadenceTaskTabView",
    "CadenceTaskListView",
    "CadenceCallTabView",
    "CadenceCallListView",
    "CadenceEmailTabView",
    "CadenceEmailListView",
]
