from rest_framework.decorators import api_view

from login.models import Datasets, Statistics, ExperimentsTypes, DocAndExperiment
from django.shortcuts import render
from django.db.models import Q

"""
get pics
"""


def get_pic_list(request):
    # get keywords
    doc_type = request.GET.get("doc_type", "")
    experiment_id = request.GET.get("experiment_id", "")
    page_number = request.GET.get("page_number", "")

    if page_number:
        current_page = int(page_number)
    else:
        current_page = 1
    page_size = 10

    query = Statistics.objects

    # todo 如果是experiment_id if type == 01 直接查所有
    #   如果 type 00 就找parent_id 直到parent_id=空

    if doc_type and experiment_id:
        dataset_flag = False
        datasets = Datasets.objects.all()
        for dataset in datasets:
            if experiment_id in dataset.dataset_id:
                dataset_flag = True
        if dataset_flag:
            experiments = ExperimentsTypes.objects.values('experiment_id').filter(
                Q(dataset_id__exact=experiment_id) & Q(path_type="01"))
            doc_list = DocAndExperiment.objects.values('doc_id').filter(experiment_id__in=experiments)
            query = query.filter(doc_id__in=doc_list)
        else:
            experiment_object = ExperimentsTypes.objects.get(experiment_id=experiment_id)
            if experiment_object.path_type == '01':
                doc_list = DocAndExperiment.objects.values('doc_id').filter(experiment_id=experiment_id)
                query = query.filter(doc_id__in=doc_list)
            else:
                # 递归找到所有的子节点
                child_list = get_child(experiment_id)
                print("===============")
                print(child_list)
                doc_list = DocAndExperiment.objects.values('doc_id').filter(experiment_id__in=child_list)
                query = query.filter(doc_id__in=doc_list)
        query = query.filter(doc_type=doc_type)
    elif experiment_id and doc_type == '':
        # todo 先判断是不是datasets节点 如果是直接搜dataset
        #  todo experiment中所有dataset_id = id的列表
        #   再查出来DocAndExperiment id list
        #     再Statistics in
        dataset_flag = False
        datasets = Datasets.objects.all()
        for dataset in datasets:
            if experiment_id in dataset.dataset_id:
                dataset_flag = True
        if dataset_flag:
            experiments = ExperimentsTypes.objects.values('experiment_id').filter(
                Q(dataset_id__exact=experiment_id) & Q(path_type="01"))
            doc_list = DocAndExperiment.objects.values('doc_id').filter(experiment_id__in=experiments)
            query = query.filter(doc_id__in=doc_list)
        else:
            experiment_object = ExperimentsTypes.objects.get(experiment_id=experiment_id)
            if experiment_object.path_type == '01':
                doc_list = DocAndExperiment.objects.values('doc_id').filter(experiment_id=experiment_id)
                query = query.filter(doc_id__in=doc_list)
            else:
                #递归找到所有的子节点
                child_list = get_child(experiment_id)
                print("===============")
                print(child_list)
                doc_list = DocAndExperiment.objects.values('doc_id').filter(experiment_id__in=child_list)
                query = query.filter(doc_id__in=doc_list)

    elif experiment_id == '' and doc_type:
        query = query.filter(doc_type=doc_type)

    start_row = (current_page - 1) * page_size
    end_row = current_page * page_size

    result = query.values('doc_id', 'filename', 'filepath', 'doc_type', 'label')[start_row:end_row]

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

def get_child(id, child_list=[]):
    ex = ExperimentsTypes.objects.get(experiment_id__exact=id)
    if ex.path_type == '01':
        child_list.append(ex.experiment_id)
    else:
        exs = ExperimentsTypes.objects.filter(parent_id=id)
        for ob in exs:
            get_child(ob.experiment_id, child_list)
    print(child_list)
    return child_list
