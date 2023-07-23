from django.shortcuts import HttpResponse
from login.models import Datasets, Statistics, ExperimentsTypes, DocAndExperiment
from django.shortcuts import render

"""
get pics
"""


def get_pic_list(request):
    # get keywords
    doc_type = request.GET.get("pic_type", "")
    experiment_id = request.GET.get("experiment_id", "")
    page_number = request.GET.get("page_number", "")

    if page_number:
        current_page = int(page_number)
    else:
        current_page = 1
    page_size = 10

    query = Statistics.objects

    if doc_type:
        query = query.filter(doc_type=doc_type)

    start_row = (current_page - 1) * page_size
    end_row = current_page * page_size

    result = query.values('id', 'filename', 'filepath', 'doc_type', 'label')[start_row:end_row]

    counts = query.count()

    total_count = 0
    if counts % page_size == 0:
        total_count = counts // page_size
    else:
        total_count = counts // page_size + 1

    if current_page > 1:
        has_previous = True
        previous_page = current_page - 1
    else:
        has_previous = False
        previous_page = current_page

    if current_page < total_count:
        has_next = True
        next_page = current_page + 1
    else:
        has_next = False
        next_page = current_page
    context = {
        "result": result,
        "page": current_page,
        "doc_type": doc_type,
        "experiment_id": experiment_id,
        "total_count": total_count,
        "has_previous": has_previous,
        "has_next": has_next,
        "previous_page": previous_page,
        "next_page": next_page,
    }
    return render(request, "plot.html", context)
