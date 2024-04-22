from django.http import HttpResponse


def healthz(request):
    return HttpResponse("OK")
