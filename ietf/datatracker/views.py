from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

from .models import DatatrackerMeta


@permission_required('wagtailadmin.access_admin')
def status(request):
    return render(request, 'datatracker/status.html', {
        'objects': DatatrackerMeta.objects.all(),
    })

