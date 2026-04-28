"""
Feature registration for the cadences app.
"""

from horilla.registry.feature import register_feature

# Register your app features and models here
register_feature(
    "cadence",
    "cadence_models",
    include_models=[
        ("leads", "Lead"),
        ("opportunities", "Opportunity"),
        ("accounts", "Account"),
        ("contacts", "Contact"),
    ],
)
