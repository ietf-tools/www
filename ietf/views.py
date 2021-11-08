from django.http import HttpResponseServerError
from django.template.loader import get_template


def server_error(request, template_name="500.html"):
    t = get_template(template_name)
    return HttpResponseServerError(t.render(locals(), request))
