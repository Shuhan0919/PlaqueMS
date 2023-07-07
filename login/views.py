import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from login import models, forms
import urllib3
import uuid
import os

"""
get proteins
"""


@csrf_exempt
def proteins_info(request):
    if request.method == 'GET':
        proteins_list = models.Proteins.objects.all()
        paginator = Paginator(proteins_list, 2)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "general.html", {"page_obj": page_obj})
    elif request.POST.get('search_protein'):
        proteins_name = request.POST.get("protein_name")
        uniprot_id = request.POST.get("uniprot_id")
        proteins_list = models.Proteins.objects.all().filter(protein_name__icontains=proteins_name).filter(
            uniprot_id__icontains=uniprot_id)

        paginator = Paginator(proteins_list, 2)  # Show 25 contacts per page.

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "general.html", {"page_obj": page_obj})


"""
get pics
"""


@csrf_exempt
def pic_info(request):
    if request.method == 'GET':
        pic_list = models.pictures.objects.all()
        paginator = Paginator(pic_list, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "plot.html", {"page_obj": page_obj})
    elif request.POST.get('search_pic'):
        # if (request.POST.get("sample_type") != '' & request.POST.get("pic_type") != ''):
        sample_type = request.POST.get("sample_type")
        pic_type = request.POST.get("pic_type")
        extraction_type = request.POST.get("extraction_type")
        sql = "select p.id, p.filename, p.filepath, p.pic_type from pictures as p left join pic_and_experiment c on p.id = c.pic_id LEFT JOIN experiments e on c.experiment_id = e.id where e.sample_type = '" + sample_type + "' and p.pic_type = '" + pic_type + "' and e.extraction_type = '" + extraction_type + "'"
        pic_list = models.pictures.objects.raw(sql)
        paginator = Paginator(pic_list, 5)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "plot.html", {"page_obj": page_obj})
    # else:
    #     print("=======================")
    #     print("bad")
    #     return render(request, "plot.html")


"""
get network cytoscape page
"""


@csrf_exempt
def network_info(request):
    return render(request, 'cytoscape.html')


"""
curl get one large network
"""


def try_curl(request):
    http = urllib3.PoolManager()
    # 发起一个GET请求并且获取请求的响应结果
    # r = http.request('GET', 'http://localhost:1234/v1/networks.json')
    r = http.request('GET', 'http://localhost:1234/v1/networks/151')
    # 输出响应的数据
    # print(r.json()[0])
    # jsonData = r.json()[0]
    jsonData = r.json()
    nodes = jsonData["elements"]["nodes"]
    edges = jsonData["elements"]["edges"]
    return render(request, "test.html", {'nodes': json.dumps(nodes), 'edges': json.dumps(edges)})


def try_curl2(request):
    http = urllib3.PoolManager()
    # 发起一个GET请求并且获取请求的响应结果
    # r = http.request('GET', 'http://localhost:1234/v1/networks.json')
    r = http.request('GET', 'http://localhost:1234/v1/networks/13656')
    # 输出响应的数据
    # print(r.json()[0])
    # jsonData = r.json()[0]
    jsonData = r.json()
    nodes = jsonData["elements"]["nodes"]
    edges = jsonData["elements"]["edges"]
    return render(request, "test2.html", {'nodes': json.dumps(nodes), 'edges': json.dumps(edges)})


# todo 数据库表！！！！！
# todo 需要一个curl去打开session带参数获取
# todo 丑一点比什么都没做强很多！


def insert(request):
    for i in range(0, 5):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        protein = models.Proteins()
        protein.id = id
        protein.uniprot_id = id
        protein.protein_name = 'protein' + str(i)
        protein.gene_symbol = ''
        # insert
        protein.save()
    return HttpResponse('insert complete')


# insert pic to mysql
# def insert_file(request):
#     folder = 'static/PlaqueMS_data/guhcl/core/ultrasound/boxplots/'
#     filenames = os.listdir(folder)
#     filepath_prefix = '../static/PlaqueMS_data/guhcl/core/ultrasound/boxplots/'
#     for filename in filenames:
#         id = str(uuid.uuid4())
#         pic = models.pictures()
#         pic.id = id
#         pic.filename = filename
#         pic.filepath = filepath_prefix + filename
#         pic.pic_type = '00'
#         pic_and_experiment = models.pic_and_experiment()
#         second_id = str(uuid.uuid4())
#         pic_and_experiment.id = second_id
#         pic_and_experiment.pic_id = id
#         pic_and_experiment.experiment_id = "1"
#         # insert
#         pic.save()
#         pic_and_experiment.save()
#     return HttpResponse('insert complete')


# def insert_file(request):
#     folder = 'static/PlaqueMS_data/guhcl/periphery/ultrasound/_bplots_crt/'
#     filenames = os.listdir(folder)
#     filepath_prefix = '../static/PlaqueMS_data/guhcl/periphery/ultrasound/_bplots_crt/'
#     for filename in filenames:
#         id = str(uuid.uuid4())
#         pic = models.pictures()
#         pic.id = id
#         pic.filename = filename
#         pic.filepath = filepath_prefix + filename
#         pic.pic_type = '00'
#         pic_and_experiment = models.pic_and_experiment()
#         second_id = str(uuid.uuid4())
#         pic_and_experiment.id = second_id
#         pic_and_experiment.pic_id = id
#         pic_and_experiment.experiment_id = "2"
#         # insert
#         pic.save()
#         pic_and_experiment.save()
#     return HttpResponse('insert complete')

def insert_file(request):
    folder = 'static/PlaqueMS_data/nacl/periphery/ultrasound/_bplots_crt/'
    filenames = os.listdir(folder)
    filepath_prefix = '../static/PlaqueMS_data/nacl/periphery/ultrasound/_bplots_crt/'
    for filename in filenames:
        id = str(uuid.uuid4())
        pic = models.pictures()
        pic.id = id
        pic.filename = filename
        pic.filepath = filepath_prefix + filename
        pic.pic_type = '00'
        pic_and_experiment = models.pic_and_experiment()
        second_id = str(uuid.uuid4())
        pic_and_experiment.id = second_id
        pic_and_experiment.pic_id = id
        pic_and_experiment.experiment_id = "3"
        # insert
        pic.save()
        pic_and_experiment.save()
    return HttpResponse('insert complete')