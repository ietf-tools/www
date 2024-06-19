from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from wagtail.contrib.search_promotions.models import Query
from wagtail.models import Page


def search(request):
    search_query = request.GET.get("query", None)
    page = request.GET.get("page", 1)

    # Search
    if search_query and "\x00" not in search_query:
        search_results = Page.objects.live().search(search_query)
        Query.get(search_query).add_hit()

    elif search_query and "\x00" in search_query:
        return HttpResponseBadRequest("Invalid search query")
    else:
        search_results = Page.objects.none()

    # Pagination
    paginator = Paginator(search_results, 10)
    try:
        search_results = paginator.page(page)
    except PageNotAnInteger:
        search_results = paginator.page(1)
    except EmptyPage:
        search_results = paginator.page(paginator.num_pages)

    return render(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": search_results,
        },
    )
