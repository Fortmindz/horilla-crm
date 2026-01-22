"""Views for handling notification-related operations."""

# Third-party imports (Django)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

# First-party / Horilla imports
from horilla_core.decorators import htmx_required

# Local application imports
from .models import Notification


class MarkNotificationReadView(LoginRequiredMixin, View):
    """View to mark a single notification as read."""

    def post(self, request, pk, *args, **kwargs):
        """
        Mark a specific notification as read.

        Args:
            request: The HTTP request object.
            pk: Primary key of the notification to mark as read.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: HTTP 200 response on success.
        """
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
            notif.read = True
            notif.save()
        except Notification.DoesNotExist:
            pass
        return HttpResponse(status=200)


class MarkAllNotificationsReadView(LoginRequiredMixin, View):
    """View to mark all notifications as read for the current user."""

    def post(self, request, *args, **kwargs):
        """
        Mark all unread notifications as read for the current user.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Rendered notification list template.
        """
        Notification.objects.filter(user=request.user, read=False).update(read=True)
        messages.success(request, "All notifications marked as read.")
        unread_notifications = Notification.objects.filter(
            user=request.user, read=False
        )
        return render(
            request,
            "notification_list.html",
            {
                "unread_notifications": unread_notifications,
            },
        )


class DeleteNotification(LoginRequiredMixin, View):
    """View to delete a single notification."""

    def post(self, request, pk, *args, **kwargs):
        """
        Delete a specific notification.

        Args:
            request: The HTTP request object.
            pk: Primary key of the notification to delete.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: HTTP 200 response on success.
        """
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
            notif.delete()
        except Notification.DoesNotExist:
            pass
        messages.success(request, "Notification Deleted.")
        response = HttpResponse(status=200)
        return response


class DeleteAllNotification(LoginRequiredMixin, View):
    """View to delete all notifications for the current user."""

    def post(self, request, *args, **kwargs):
        """
        Delete all notifications for the current user.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Rendered sidebar list template.
        """
        Notification.objects.filter(user=request.user).delete()
        messages.success(request, f"All notifications cleared.")
        return render(request, "sidebar_list.html", {"request": request})


@method_decorator(htmx_required, name="dispatch")
class OpenNotificationView(LoginRequiredMixin, View):
    """View to open a notification and redirect to its associated URL."""

    def get(self, request, pk, *args, **kwargs):
        """
        Mark a notification as read and redirect to its URL.

        Args:
            request: The HTTP request object.
            pk: Primary key of the notification to open.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Response with HX-Redirect header or error page.
        """
        try:
            notif = Notification.objects.get(pk=pk, user=request.user)
            notif.is_read = True
            notif.save()

            response = HttpResponse()
            response["HX-Redirect"] = notif.url
            return response

        except Notification.DoesNotExist:
            return render(request, "error/403.html", status=404)
