import json

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from login import models
import random

"""
get proteins
"""


@csrf_exempt
def proteins_info(request):
    if request.method == 'GET':
        proteins_list = models.Proteins.objects.all()
        return render(request, 'general.html', locals())
    elif request.POST.get('search_protein'):
        proteins_name = request.POST.get("protein_name")
        uniprot_id = request.POST.get("uniprot_id")
        proteins_list = models.Proteins.objects.all().filter(protein_name__icontains=proteins_name).filter(
            uniprot_id__icontains=uniprot_id)
        return render(request, 'general.html', locals())


"""
get pics
"""


@csrf_exempt
def pic_info(request):
    return render(request, 'plot.html')


"""
get networks
"""


@csrf_exempt
def network_info(request):
    return render(request, 'cytoscape.html')


"""
insert fake data
"""


def insert(request):
    for i in range(0, 5):
        id = int(random.uniform(0, 1) * 10000000000)
        protein = models.Proteins()
        protein.id = id
        protein.uniprot_id = id
        protein.protein_name = 'protein' + str(i)
        protein.gene_symbol = ''
        # insert
        protein.save()
    return HttpResponse('insert complete')


def show_relationships(request):
    return render(request, 'general.html')


# @swagger_auto_schema(method='get')
# @action(methods=['get'], detail=False)
# def getData(self,request):
#     data = request.elements
#     return
# import json
# def eg(request):
#     data = request.data
#     return render(request,"test.html",{"data":json.dumps(data)})

"""
分页 还没做
"""
# def data(res):
#     messages = table1.objects.all()  # 获取全部数据
#     limit = 20
#     paginator = Paginator(messages, limit)  # 按每页10条分页
#     page = res.GET.get('page', '1')  # 默认跳转到第一页
#     result = paginator.page(page)
#     return render(res, 'data.html', {'messages': result,'op1':'active'})

"""
curl
"""
import urllib3


def try_curl(request):
    http = urllib3.PoolManager()
    # 发起一个GET请求并且获取请求的响应结果
    r = http.request('GET', 'http://localhost:1234/v1/networks.json')
    #输出响应的数据
    # print(r.json()[0])
    jsonData = r.json()[0]
    nodes = jsonData["elements"]["nodes"]
    edges = jsonData["elements"]["edges"]
    return render(request, "test.html", {'nodes':json.dumps(nodes),'edges':json.dumps(edges)})
