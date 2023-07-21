from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from login.models import proteins, statistics
from django.db.models import Q

"""
get proteins
"""


@api_view(['GET'])
@csrf_exempt
def proteins_info(request):
    # get all the list
    proteins_list = proteins.objects.all()
    # get keywords
    uniprotkb_id = request.GET.get("uniprotkb_id", "")
    gene_name = request.GET.get("gene_name", "")
    if gene_name and uniprotkb_id:
        name_search_list = gene_name.split(",")
        name_search = ",".join('"' + item + '"' for item in name_search_list)
        id_search_list = uniprotkb_id.split(",")
        id_search = ",".join('"' + item + '"' for item in id_search_list)
        sql = 'SELECT p.id, p.uniprot_accession_id, p.uniprotkb_id, p.gene_name FROM proteins p ' \
              'WHERE p.gene_name in (' + name_search + ')' + 'OR p.uniprotkb_id IN (' + id_search + ')'
        proteins_list = proteins.objects.raw(sql)
    elif uniprotkb_id and gene_name == '':
        id_search_list = uniprotkb_id.split(",")
        id_search = ",".join('"' + item + '"' for item in id_search_list)
        sql = 'SELECT p.id, p.uniprot_accession_id, p.uniprotkb_id, p.gene_name FROM proteins p ' \
              'WHERE p.uniprotkb_id IN (' + id_search + ')'
        proteins_list = proteins.objects.raw(sql)
    elif uniprotkb_id == '' and gene_name:
        name_search_list = gene_name.split(",")
        name_search = ",".join('"' + item + '"' for item in name_search_list)
        sql = 'SELECT p.id, p.uniprot_accession_id, p.uniprotkb_id, p.gene_name FROM proteins p ' \
              'WHERE p.gene_name in (' + name_search + ')'
        proteins_list = proteins.objects.raw(sql)
    # begin pagination
    paginator = Paginator(proteins_list, 2)
    page_num = request.GET.get('page_num', 1)
    try:
        result_page = paginator.page(page_num)  # result_page is a page object
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result_page = paginator.page(paginator.num_pages)
    page_range = paginator.page_range
    page_last = paginator.num_pages
    context = {
        "result_page": result_page,
        "page_range": page_range,
        "page_last": page_last,
        "gene_name": gene_name,
        "uniprotkb_id": uniprotkb_id,
    }
    return render(request, "general.html", context)


@csrf_exempt
def show_list(request):
    # get keywords
    uniprotkb_id = request.GET.get("uniprotkb_id", "")
    gene_name = request.GET.get("gene_name", "")
    page_number = request.GET.get("page_number", "")

    if page_number:
        current_page = int(page_number)
    else:
        current_page = 1
    page_size = 10

    query = proteins.objects

    if gene_name and uniprotkb_id:
        name_search_list = gene_name.split(",")
        id_search_list = uniprotkb_id.split(",")
        query = query.filter(Q(uniprotkb_id__in=id_search_list) | Q(gene_name__in=name_search_list))

    elif uniprotkb_id and gene_name == '':
        id_search_list = uniprotkb_id.split(",")
        query = query.filter(uniprotkb_id__in=id_search_list)

    elif uniprotkb_id == '' and gene_name:
        name_search_list = gene_name.split(",")
        query = query.filter(gene_name__in=name_search_list)

    start_row = (current_page - 1) * page_size
    end_row = current_page * page_size

    result = query.values('id', 'uniprot_accession_id', 'uniprotkb_id', 'gene_name')[start_row:end_row]

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
        "gene_name": gene_name,
        "uniprotkb_id": uniprotkb_id,
        "total_count": total_count,
        "has_previous": has_previous,
        "has_next": has_next,
        "previous_page": previous_page,
        "next_page": next_page,
    }
    return render(request, "general.html", context)


"""
get pics
"""


@csrf_exempt
def pic_info(request):
    if request.method == 'GET':
        pic_list = statistics.objects.all()
        paginator = Paginator(pic_list, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "plot.html", {"page_obj": page_obj})
        # elif request.POST.get('search_pic'):
        #     # if (request.POST.get("sample_type") != '' & request.POST.get("pic_type") != ''):
        #     sample_type = request.POST.get("sample_type")
        #     pic_type = request.POST.get("pic_type")
        #     extraction_type = request.POST.get("extraction_type")
        #     sql = "select p.id, p.filename, p.filepath, p.pic_type from pictures as p left join pic_and_experiment c on " \
        #           "p.id = c.pic_id LEFT JOIN experiments e on c.experiment_id = e.id where e.sample_type = '" + \
        #           sample_type + "' and p.pic_type = '" + pic_type + "' and e.extraction_type = '" + extraction_type + "'"
        #     pic_list = models.pictures.objects.raw(sql)
        #     paginator = Paginator(pic_list, 5)
        #     page_number = request.GET.get("page")
        #     page_obj = paginator.get_page(page_number)
        return render(request, "plot.html", {"page_obj": page_obj})
    # else:
    #     print("=======================")
    #     print("bad")
    #     return render(request, "plot.html")


# views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
