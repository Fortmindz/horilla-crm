"""
Signal handlers for the horilla_calendar app.

This module defines Django signal receivers related to calendar functionality,
for example creating default shortcut keys for newly created users, and
automatic syncing of Horilla events to each user's Google Calendar.
"""

import logging
import threading

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


def _run_in_thread(fn, *args, **kwargs):
    """Fire-and-forget: run fn(*args) in a daemon thread so the request returns immediately."""
    t = threading.Thread(target=fn, args=args, kwargs=kwargs, daemon=True)
    t.start()


from horilla.auth.models import User
from horilla.urls import reverse_lazy
from horilla_keys.models import ShortcutKey

logger = logging.getLogger(__name__)


# Define your  signals here
@receiver(post_save, sender=User)
def create_calendar_shortcuts(sender, instance, created, **kwargs):
    """
    Add default calendar shortcut keys for newly created users.

    This signal handler runs after a User is saved and ensures that a predefined
    set of `ShortcutKey` entries exist for the user (creates them if missing).
    """
    predefined = [
        {
            "page": str(reverse_lazy("horilla_calendar:calendar_view")),
            "key": "I",
            "command": "alt",
        },
    ]

    for item in predefined:
        ShortcutKey.all_objects.get_or_create(
            user=instance,
            key=item["key"],
            command=item["command"],
            defaults={
                "page": item["page"],
                "company": instance.company,
            },
        )


# ---------------------------------------------------------------------------
# Google Calendar sync signals
# ---------------------------------------------------------------------------


def _sync_activity(instance):
    """Push an Activity to Google Calendar for all related users who are connected."""
    from horilla_calendar.google_calendar.sync import push_activity_to_google

    users = set()
    if instance.owner_id:
        users.add(instance.owner)
    if instance.meeting_host_id:
        users.add(instance.meeting_host)
    try:
        for u in instance.assigned_to.all():
            users.add(u)
    except Exception:
        pass

    for user in users:
        try:
            push_activity_to_google(instance, user)
        except Exception as exc:
            logger.error(
                "Google sync error for activity %s user %s: %s", instance.pk, user, exc
            )


@receiver(post_save, sender="horilla_activity.Activity")
def sync_activity_to_google(sender, instance, **kwargs):
    """Auto-push Activity to Google Calendar on create/update.
    Runs in a background thread so the request returns immediately.
    Skip activities pulled FROM Google to avoid a sync loop.
    """
    from horilla_calendar.google_calendar.sync import is_pulling_from_google

    if getattr(instance, "_from_google", False) or is_pulling_from_google():
        return
    _run_in_thread(_sync_activity, instance)


@receiver(post_delete, sender="horilla_activity.Activity")
def delete_activity_from_google(sender, instance, **kwargs):
    """Remove Activity from Google Calendar when deleted from Horilla.
    Runs in a background thread so the delete response is instant.
    """
    from horilla_calendar.google_calendar.sync import delete_activity_google_event

    user = instance.owner
    if not user:
        return

    def _do_delete():
        try:
            delete_activity_google_event(instance, user)
        except Exception as exc:
            logger.error(
                "Google delete error for activity %s user %s: %s",
                instance.pk,
                user,
                exc,
            )

    _run_in_thread(_do_delete)


@receiver(post_save, sender="horilla_calendar.UserAvailability")
def sync_unavailability_to_google(sender, instance, **kwargs):
    """Auto-push UserAvailability block to Google Calendar on create/update.
    Runs in a background thread. Skip records pulled FROM Google to avoid a sync loop.
    """
    if instance.reason and instance.reason.startswith("[Google]"):
        return

    from horilla_calendar.google_calendar.sync import push_unavailability_to_google

    def _do_push():
        try:
            push_unavailability_to_google(instance)
        except Exception as exc:
            logger.error(
                "Google sync error for unavailability %s: %s", instance.pk, exc
            )

    _run_in_thread(_do_push)


@receiver(post_delete, sender="horilla_calendar.UserAvailability")
def delete_unavailability_from_google(sender, instance, **kwargs):
    """Remove UserAvailability block from Google Calendar when deleted.
    Runs in a background thread. Skip [Google]-sourced records.
    """
    if instance.reason and instance.reason.startswith("[Google]"):
        return

    from horilla_calendar.google_calendar.sync import delete_unavailability_google_event

    def _do_delete():
        try:
            delete_unavailability_google_event(instance)
        except Exception as exc:
            logger.error(
                "Google delete error for unavailability %s: %s", instance.pk, exc
            )

    _run_in_thread(_do_delete)
