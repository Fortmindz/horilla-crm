"""Cadence follow-up create/update/delete views."""

from functools import cached_property

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from horilla.http import HttpResponse
from horilla.urls import reverse_lazy
from horilla.utils.decorators import (
    htmx_required,
    method_decorator,
    permission_required_or_denied,
)
from horilla.utils.translation import gettext_lazy as _
from horilla_cadences.forms import CadenceFollowUpForm
from horilla_cadences.models import Cadence, CadenceFollowUp
from horilla_generics.views import HorillaSingleDeleteView, HorillaSingleFormView
from horilla_mail.models import HorillaMailConfiguration


@method_decorator(htmx_required, name="dispatch")
@method_decorator(
    permission_required_or_denied(["horilla_cadences.add_cadence"]), name="dispatch"
)
class CadenceFollowUpCreateView(LoginRequiredMixin, HorillaSingleFormView):
    """Create follow-up item for a cadence."""

    model = CadenceFollowUp
    form_class = CadenceFollowUpForm
    modal_height = False
    save_and_new = False
    view_id = "cadence-followup-form"
    hidden_fields = ["followup_number", "branch_from"]

    @staticmethod
    def _has_outgoing_mail_server(cadence):
        qs = HorillaMailConfiguration.all_objects.filter(
            mail_channel="outgoing", is_active=True
        )
        if (
            cadence
            and cadence.company_id
            and qs.filter(company_id=cadence.company_id).exists()
        ):
            return True
        return qs.filter(is_primary=True).exists() or qs.exists()

    def _should_show_mail_config_popup(self, request, **kwargs):
        followup_type = request.GET.get("followup_type")
        is_update = bool(kwargs.get("pk"))
        if followup_type != "email" or is_update:
            return False
        cadence_pk = kwargs.get("cadence_pk") or request.GET.get("cadence")
        cadence = (
            Cadence.objects.only("id", "company_id").filter(pk=cadence_pk).first()
            if cadence_pk
            else None
        )
        return not self._has_outgoing_mail_server(cadence)

    def get(self, request, *args, **kwargs):
        show_mail_config_popup = self._should_show_mail_config_popup(request, **kwargs)
        if show_mail_config_popup:
            query = request.GET.copy()
            query["followup_type"] = "task"
            request.GET = query
        response = super().get(request, *args, **kwargs)
        if show_mail_config_popup and isinstance(response, HttpResponse):
            if hasattr(response, "render") and callable(response.render):
                response = response.render()
            popup_script = render_to_string(
                "partials/cadence_mail_config_popup.html",
                {"configure_url": "/mail/mail-server/"},
                request=request,
            )
            response.content = response.content + popup_script.encode("utf-8")
        return response

    def get_initial(self):
        initial = super().get_initial()
        if self.kwargs.get("pk"):
            return initial
        cadence_pk = self.kwargs.get("cadence_pk")
        if cadence_pk:
            initial["cadence"] = cadence_pk
        if self.request.GET.get("followup_number"):
            initial["followup_number"] = self.request.GET.get("followup_number")
        if self.request.GET.get("followup_type"):
            initial["followup_type"] = self.request.GET.get("followup_type")
        if self.request.GET.get("branch_from"):
            initial["branch_from"] = self.request.GET.get("branch_from")
        return initial

    @cached_property
    def form_url(self):
        if self.kwargs.get("pk"):
            return reverse_lazy(
                "cadences:cadence_followup_update_view",
                kwargs={"pk": self.kwargs.get("pk")},
            )
        cadence_pk = self.kwargs.get("cadence_pk")
        return reverse_lazy(
            "cadences:cadence_followup_create_view",
            kwargs={"cadence_pk": cadence_pk},
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        form_url = self.get_form_url()
        if hasattr(form_url, "url"):
            form_url = form_url.url
        kwargs["form_url"] = self.request.build_absolute_uri(form_url)
        kwargs["htmx_trigger_target"] = f"#{self.view_id}-container"
        kwargs["do_this_toggle_url"] = reverse_lazy(
            "cadences:cadence_followup_do_this_value_field"
        )
        return kwargs

    def form_valid(self, form):
        super().form_valid(form)
        return HttpResponse("<script>closeModal();$('#reloadButton').click();</script>")


@method_decorator(htmx_required, name="dispatch")
@method_decorator(
    permission_required_or_denied(
        [
            "horilla_cadences.delete_cadencefollowup",
        ]
    ),
    name="dispatch",
)
class CadenceFollowUpDeleteView(LoginRequiredMixin, HorillaSingleDeleteView):
    """Delete follow-up when it has no branch children."""

    model = CadenceFollowUp
    check_delete_permission = False
    success_message = _("Follow-up removed.")

    def _block_if_has_branch_children(self):
        if self.object.branch_children.exists():
            messages.error(
                self.request,
                _(
                    "Remove or reassign follow-ups in later stages before deleting this step."
                ),
            )
            return HttpResponse(
                "<script>closeModal();$('#reloadButton').click();$('#reloadMessagesButton').click();</script>"
            )
        return None

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise
        blocked = self._block_if_has_branch_children()
        if blocked is not None:
            return blocked
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            raise
        blocked = self._block_if_has_branch_children()
        if blocked is not None:
            return blocked
        return super().post(request, *args, **kwargs)

    def get_post_delete_response(self):
        return HttpResponse(
            "<script>closeModal();htmx.trigger('#reloadButton','click');"
            "$('#reloadMessagesButton').click();closeDeleteModeModal();closeDeleteModal();</script>"
        )


@method_decorator(htmx_required, name="dispatch")
class CadenceFollowupDoThisValueFieldView(LoginRequiredMixin, TemplateView):
    """Return only do_this_value field container (HTMX field-level update)."""

    template_name = "partials/cadence_followup_do_this_value_field.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CadenceFollowUpForm(
            initial=self.request.GET.dict() if self.request.GET else None
        )
        context["form"] = form
        do_this_unit = self.request.GET.get("do_this_unit") or "immediately"
        context["show_field"] = do_this_unit != "immediately"
        return context
