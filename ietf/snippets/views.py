from django.conf import settings
from django.shortcuts import get_object_or_404, render

from .models import MailingListSignup


def disclaimer(request, signup_id):
    signup = get_object_or_404(MailingListSignup, pk=signup_id)

    return render(
        request,
        "snippets/disclaimer.html",
        {"url": signup.link, "note_well_git_url": settings.NOTE_WELL_REPO},
    )
