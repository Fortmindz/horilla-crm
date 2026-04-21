"""
Filters for the cadences app
"""

# First party imports (Horilla)
from horilla.db.models import Exists, OuterRef, Q

# First-party / Horilla apps
from horilla_cadences.models import Cadence
from horilla_core.mixins import OwnerFiltersetMixin
from horilla_generics.filters import HorillaFilterSet


class CadenceFilter(OwnerFiltersetMixin, HorillaFilterSet):
    """
    cadence filter
    """

    class Meta:
        """
        meta class for Review Process Filter
        """

        model = Cadence
        fields = "__all__"
        exclude = ["additional_info", "id", "review_fields"]
        search_fields = ["name", "module__model", "module__app_label"]
