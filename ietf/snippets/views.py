from django.shortcuts import get_object_or_404, render

from ietf.utils.models import TextChunk

from .models import MailingListSignup


def disclaimer(request, signup_id):
    signup = get_object_or_404(MailingListSignup, pk=signup_id)
    note_well, created = TextChunk.objects.get_or_create(slug="note-well")

    return render(
        request,
        "snippets/disclaimer.html",
        {"url": signup.link, "note_well": note_well},
    )
