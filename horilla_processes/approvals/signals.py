"""Signals for approvals job syncing and edit guards."""

# Third-party imports (Django)
from django.db import transaction
from django.db.models.signals import post_delete, post_save, pre_save

# First-party / Horilla imports
from horilla.registry.feature import FEATURE_REGISTRY
from horilla_utils.middlewares import _thread_local

# Local imports
from .utils import enforce_pending_edit_policy, sync_approval_instances_for_record


def _approval_models():
    return FEATURE_REGISTRY.get("approval_models", [])


def _is_approval_internal_model(model):
    return model._meta.app_label == "approvals"


def _on_registered_model_saved(sender, instance, created, **kwargs):
    """
    Run approval matching after the DB transaction commits.

    This lets the review-process post_save (and any other listeners) finish in the
    same transaction first, so pending ReviewJob rows exist when we evaluate
    """
    if getattr(_thread_local, "skip_approval_sync", False):
        return
    pk = getattr(instance, "pk", None)
    if pk is None:
        return

    def _sync():
        try:
            obj = sender.objects.get(pk=pk)
        except sender.DoesNotExist:
            return
        sync_approval_instances_for_record(obj, created=created)

    transaction.on_commit(_sync)


def _on_registered_model_pre_save(sender, instance, **kwargs):
    enforce_pending_edit_policy(instance)


def _on_registered_model_deleted(sender, instance, **kwargs):
    from horilla_core.models import HorillaContentType

    from .models import ApprovalInstance

    try:
        content_type = HorillaContentType.objects.get_for_model(sender)
        ApprovalInstance.objects.filter(
            content_type=content_type,
            object_id=str(instance.pk),
        ).delete()
    except Exception:
        pass


def _connect_registered_models():
    for model in _approval_models():
        if _is_approval_internal_model(model):
            continue
        post_save.connect(
            _on_registered_model_saved,
            sender=model,
            dispatch_uid=f"approvals_post_save_{model._meta.label_lower}",
        )
        pre_save.connect(
            _on_registered_model_pre_save,
            sender=model,
            dispatch_uid=f"approvals_pre_save_{model._meta.label_lower}",
        )
        post_delete.connect(
            _on_registered_model_deleted,
            sender=model,
            dispatch_uid=f"approvals_post_delete_{model._meta.label_lower}",
        )


def _patch_horilla_list_view():
    """Patch list querysets at runtime without editing generics code."""
    try:
        from horilla_core.models import HorillaContentType
        from horilla_generics.views.list import HorillaListView

        from .models import ApprovalInstance
    except Exception:
        return

    if getattr(HorillaListView, "_approval_list_patch_applied", False):
        return

    original_get_queryset = HorillaListView.get_queryset

    def patched_get_queryset(self):
        queryset = original_get_queryset(self)
        model = getattr(self, "model", None)
        if not model or model._meta.app_label == "approvals":
            return queryset
        try:
            content_type = HorillaContentType.objects.get_for_model(model)
            pending_object_ids = ApprovalInstance.objects.filter(
                content_type=content_type,
                status__in=["pending", "rejected"],
                is_active=True,
            ).values_list("object_id", flat=True)
            return queryset.exclude(pk__in=pending_object_ids)
        except Exception:
            return queryset

    HorillaListView.get_queryset = patched_get_queryset
    HorillaListView._approval_list_patch_applied = True


_connect_registered_models()
_patch_horilla_list_view()
