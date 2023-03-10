from django.shortcuts import get_object_or_404, render

from ietf.standard.models import StandardPage

from .models import MailingListSignup


def disclaimer(request, signup_id):
    signup = get_object_or_404(MailingListSignup, pk=signup_id)
    note_well = StandardPage.objects.filter(slug="note-well").first()

    return render(
        request,
        "snippets/disclaimer.html",
        {"url": signup.link, "note_well": note_well},
    )
