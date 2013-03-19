from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

PAGE_SIZE = 20

def page_queryset(q, p):
    paginator = Paginator(q, PAGE_SIZE)
    try:
        queryset = paginator.page(p)
    except PageNotAnInteger:
        queryset = paginator.page(1)
    except EmptyPage:
        queryset = paginator.page(paginator.num_pages)
    return queryset
