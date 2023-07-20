import json

from django.forms import model_to_dict
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from login import models, forms
import urllib3
import uuid
import os

"""
get proteins
"""


@csrf_exempt
def proteins_info(request):
    # get all the list
    proteins_list = models.proteins.objects.all()
    # get keywords
    protein_name = request.GET.get("protein_name", "")
    uniprot_id = request.GET.get("uniprot_id", "")
    if protein_name and uniprot_id:
        name_search_list = protein_name.split(",")
        name_search = ",".join('"' + item + '"' for item in name_search_list)
        id_search_list = uniprot_id.split(",")
        id_search = ",".join('"' + item + '"' for item in id_search_list)
        sql = 'SELECT p.id, p.uniprot_id, p.protein_name, p.gene_symbol FROM proteins p ' \
              'WHERE p.protein_name in (' + name_search + ')' + 'OR p.uniprot_id IN (' + id_search + ')'
        proteins_list = models.proteins.objects.raw(sql)
    elif uniprot_id and protein_name == '':
        id_search_list = uniprot_id.split(",")
        id_search = ",".join('"' + item + '"' for item in id_search_list)
        sql = 'SELECT p.id, p.uniprot_id, p.protein_name, p.gene_symbol FROM proteins p ' \
              'WHERE p.uniprot_id IN (' + id_search + ')'
        proteins_list = models.proteins.objects.raw(sql)
    elif uniprot_id == '' and protein_name:
        name_search_list = protein_name.split(",")
        name_search = ",".join('"' + item + '"' for item in name_search_list)
        sql = 'SELECT p.id, p.uniprot_id, p.protein_name, p.gene_symbol FROM proteins p ' \
              'WHERE p.protein_name in (' + name_search + ')'
        proteins_list = models.proteins.objects.raw(sql)
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
        "protein_name": protein_name,
        "uniprot_id": uniprot_id,
    }
    return render(request, "general.html", context)


"""
get pics
"""


@csrf_exempt
def pic_info(request):
    if request.method == 'GET':
        pic_list = models.statistics.objects.all()
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


# @csrf_exempt
# def get_pic_info(request):
#     # get all the list
#     pictures_list = models.pictures.objects.all()
#     # get keywords
#     pic_type = request.GET.get("pic_type", "")
#     extraction_type = request.GET.get("extraction_type", "")
#     # pic_type = request.GET.get("pic_type", "")
#     sample_type = request.GET.get("sample_type", "")
#     if pic_type:
#         pictures_list = pictures_list.filter(pic_type__exact=pic_type)
#     if extraction_type:
#         pictures_list = pictures_list.filter(uniprot_id__icontains=uniprot_id)
#     # begin pagination
#     paginator = Paginator(proteins_list, 2)
#     page_num = request.GET.get('page_num', 1)
#     try:
#         result_page = paginator.page(page_num)  # result_page is a page object
#     except PageNotAnInteger:
#         # If page is not an integer, deliver first page.
#         result_page = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range (e.g. 9999), deliver last page of results.
#         result_page = paginator.page(paginator.num_pages)
#     page_range = paginator.page_range
#     page_last = paginator.num_pages
#     context = {
#         "result_page": result_page,
#         "page_range": page_range,
#         "page_last": page_last,
#         "protein_name": protein_name,
#         "uniprot_id": uniprot_id,
#     }
#     return render(request, "general.html", context)


"""
get network cytoscape page
"""


@csrf_exempt
def network_info(request):
    return render(request, 'cytoscape.html')


from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import GoodsSerializer
from django.core.paginator import Paginator, EmptyPage, InvalidPage


class GoodsPageApi(APIView):
    """
    分页
    """

    def get(self, request, pindex):
        # 1、获取商品信息
        goods_list = models.proteins.objects.all()
        # 2、实例化分页器
        paginat = Paginator(goods_list, 2)
        # 3、 获取分页
        paged = paginat.page(pindex)
        try:  # 判断是否有下一页
            paged.has_next()
            down_page = paged.next_page_number()  # 获取一下页的页码
        except EmptyPage:  # 如果下一页为空的话，
            down_page = paged.paginator.num_pages  # 获取最后一页的页码
            paged = paginat.page(down_page)

        try:
            paged.has_previous()  # 判断是否有上一页
            up_page = paged.previous_page_number()  # 获取上页的页码
        except InvalidPage:  # 如果没有上一页
            up_page = 1  # 返回第一页
            paged = paginat.page(up_page)

        # 4、 做序列化
        page_serializer = GoodsSerializer(paged, many=True)

        # 5、 返回数据
        return Response({
            'code': 200,
            'data': page_serializer.data,
            'page_list': [i for i in paginat.page_range],
            'num_pages': paginat.num_pages,
            'has_previous': paged.has_previous(),  # 判断是否有上一页
            'has_next': paged.has_next(),  # 判断是否有下一页
            'previous_page_number': up_page,  # 返回上一页的页码
            'next_page_number': down_page,  # 返回下一页的页码
            'page_number': paged.number  # 返回当前页页码
        })


def get_proteins(request):
    # return render(request, 'fenye.html')
    page_num = "1"
    if (request.GET.get("page_num")):
        page_num = request.GET.get("page_num")
    http = urllib3.PoolManager()
    # 发起一个GET请求并且获取请求的响应结果
    r = http.request('GET', 'http://127.0.0.1:8000/goods_page/' + page_num)
    jsonData = r.json()
    # print(json.dumps(jsonData))
    data = jsonData["data"]
    num_pages = jsonData["num_pages"]
    has_previous = jsonData["has_previous"]
    has_next = jsonData["has_next"]
    page_number = jsonData["page_number"]
    return render(request, "fenye.html",
                  {'data': data, 'num_pages': int(num_pages),
                   'has_previous': bool(has_previous),
                   'has_next': bool(has_next), 'page_number': int(page_number)})


# views.py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger