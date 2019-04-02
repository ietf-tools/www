from django.contrib.auth.decorators import permission_required
from django.core.management import call_command
from django.shortcuts import get_object_or_404, redirect, render
from django_q.tasks import async
from wagtail.admin import messages

from .models import DatatrackerMeta


@permission_required('wagtailadmin.access_admin')
def status(request):
    id = request.POST.get('id')
    if id:
        cls = get_object_or_404(DatatrackerMeta, pk=id).content_type.model_class()
        async(fetch_and_update, cls, hook=call_update_index_no_datatracker)
        messages.success(request, "Updating %s" % cls.__name__)
        redirect('status')
    return render(request, 'datatracker/status.html', {
        'objects': DatatrackerMeta.objects.all(),
    })


def call_update_index_no_datatracker(task):
    call_command('update_index_no_datatracker')


def fetch_and_update(cls):
    cls.fetch_and_update()
