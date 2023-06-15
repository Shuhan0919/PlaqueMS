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
        return render(request, 'index.html',locals())
    elif request.POST.get('search_protein'):
        proteins_name = request.POST.get("protein_name")
        proteins_list = models.Proteins.objects.all().filter(protein_name__icontains=proteins_name)
        return render(request, 'index.html', locals())

# def proteins_data(request):
#     if request.GET.get("proteins_data") is not None:
#         protein_name = request.GET['protein_name']
#         protein_list = models.Proteins.objects.filter(protein_name=protein_name)
#         if len(protein_list) > 0:     # 数据库中存在
#             return render(request, 'index.html', {"protein_list": protein_list})
#         else:      # 数据库中不存在
#             error_content = {'error': 'sorry! No result found'}
#             return render(request, 'index.html', error_content)
#     else:
#         protein_list = models.Proteins.objects.all()
#         return render(request, 'index.html', {"protein_list": protein_list})

"""
insert fake data
"""
def insert(request):
    for i in range(0, 5):
        id = int(random.uniform(0, 1) * 10000000000)
        protein = models.Proteins()
        protein.id = id
        protein.uniprot_id = id
        protein.protein_name =  'protein' + str(i)
        protein.gene_symbol = ''
        # insert
        protein.save()
    return HttpResponse('insert complete')
