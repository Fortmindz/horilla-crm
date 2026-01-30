"""
Feature registration for Horilla Core app.
"""

from horilla.auth.models import User
from horilla.registry.feature import register_models_for_feature
from horilla_core.models import Company, Department, Role

register_models_for_feature(
    models=[
        Company,
        Department,
        Role,
        User,
    ],
    all=True,
    exclude=["dashboard_component", "report_choices"],
)
