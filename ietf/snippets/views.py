import json

from django.contrib.auth.decorators import permission_required
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from wagtail.utils.pagination import paginate
from wagtail.admin.forms import SearchForm
from wagtail.admin.modal_workflow import render_modal_workflow
from wagtail.core import hooks
from wagtail.search.backends import get_search_backend

from .models import MailingListSignup


def disclaimer(request, signup_id):
    signup = get_object_or_404(MailingListSignup, pk=signup_id)
    return render(request, "snippets/disclaimer.html", {'url': signup.link})


_choosers_by_type = None


def find_choosers():
    global _choosers_by_type

    if _choosers_by_type is None:
        _choosers_by_type = {}
        for hook in hooks.get_hooks('register_link_chooser'):
            handler = hook()
            _choosers_by_type[handler.link_type] = handler

    return _choosers_by_type


@permission_required('wagtailadmin.access_admin')
def chooser(request, snippet_type=None):
    try:
        handler = find_choosers()[snippet_type]
    except KeyError:
        raise Http404
    model = handler.model
    if 'q' in request.GET or 'p' in request.GET:
        searchform = SearchForm(request.GET)

        if searchform.is_valid():
            s = get_search_backend()
            q = searchform.cleaned_data['q']

            items = s.search(q, model.objects.all())
            is_searching = True
        else:
            q = request.GET.get('q', '')
            items = model.objects.all()
            is_searching = False

        # Pagination
        _, items = paginate(
            request,
            items,
            per_page=10
        )

        return render(request, 'snippets/includes/_results.html', {
            'items': items,
            'snippet_type': handler,
            'query_string': q,
            'is_searching': is_searching,
        })

    searchform = SearchForm()

    items = model.objects.all()
    _, items = paginate(
        request,
        items,
        per_page=10
    )

    return render_modal_workflow(
        request,
        'snippets/browse.html',
        'snippets/chooser.js',
        {
            'SNIPPET_TYPES': find_choosers(),
            'items': items,
            'searchform': searchform,
            'snippet_type': handler,
        }
    )


@permission_required('wagtailadmin.access_admin')
def chosen(request, snippet_type, item_id):
    chooser = find_choosers()[snippet_type]
    model = chooser.model
    item = get_object_or_404(model, id=item_id)

    return render_modal_workflow(
        request, None, 'snippets/chosen.js',
        {'json': json.dumps({
            'url': item.url,
            'data': {
                'id': item_id,
            },
            'title': item.title,
            'type': chooser.link_type
        })}
    )
