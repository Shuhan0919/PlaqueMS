import json

from django.http import Http404
from django.shortcuts import render, HttpResponse
import urllib3
import pandas as pd
import py4cytoscape as p4c
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
import requests
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from login.models import Networks, Statistics


def try_curl(request):
    return render(request, "network.html")


# todo import network
# @api_view(['GET'])
@csrf_exempt
@api_view(['GET', 'POST'])
def create_network(request):
    network_id = request.GET.get("network_id", "")

    network = Networks.objects.get(network_id=network_id)
    print(network.filepath)

    gu_core_data = pd.read_table(network.filepath)

    edge_data = {'source': gu_core_data["Regulator"],
                 'target': gu_core_data["Target"],
                 'MI': gu_core_data["MI"],
                 'pvalue': gu_core_data["pvalue"],
                 'directionality': gu_core_data["directionality"]
                 }
    edges = pd.DataFrame(data=edge_data, columns=['source', 'target', 'MI', 'pvalue', 'directionality'])
    p4c.create_network_from_data_frames(edges=edges, title=network.filename, collection=network.filename)

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_data = {'network': 'current'}

    response = requests.post('http://localhost:1234/v1/commands/network/get', headers=headers, json=json_data)
    suid = response.json()["data"]["SUID"]

    http = urllib3.PoolManager()
    r = http.request('GET', 'http://localhost:1234/v1/networks/' + str(suid))
    jsonData = r.json()
    nodes = jsonData["elements"]["nodes"]
    edges = jsonData["elements"]["edges"]

    http_style = urllib3.PoolManager()
    r_style = http_style.request('GET', 'http://localhost:1234/v1/styles/default.json')
    json_style = r_style.json()
    style = json_style[0]["style"]
    return Response({'nodes': nodes, 'edges': edges, 'style': style})
    # return HttpResponse("success")


@api_view(['GET'])
def do_mcl(request):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_mcl = {
        "adjustLoops": "true",
        "attribute": "pvalue",
        "clusterAttribute": "mclCluster",
        "clusteringThresh": "1e-15",
        "createGroups": "false",
        "createNewClusteredNetwork": "true",
        "edgeWeighter": "1-value",
        "forceDecliningResidual": "true",
        "inflation_parameter": "2.5",
        "iterations": "16",
        "maxResidual": "0.001",
        "selectedOnly": "false",
        "undirectedEdges": "true"
    }

    res = requests.post('http://localhost:1234/v1/commands/cluster/mcl', headers=headers, json=json_mcl)

    # if response.status_code == 200:
    json_data = {'network': 'current'}

    response = requests.post('http://localhost:1234/v1/commands/network/get', headers=headers, json=json_data)
    suid = response.json()["data"]["SUID"]

    http = urllib3.PoolManager()
    r = http.request('GET', 'http://localhost:1234/v1/networks/' + str(suid))
    jsonData = r.json()
    nodes = jsonData["elements"]["nodes"]
    edges = jsonData["elements"]["edges"]

    http_style = urllib3.PoolManager()
    r_style = http_style.request('GET', 'http://localhost:1234/v1/styles/default.json')
    json_style = r_style.json()
    style = json_style[0]["style"]

    return Response({'nodes': nodes, 'edges': edges, 'style': style})


# # get networks file and Statistics file
# @api_view(['GET'])
# def file_info(request):
#     return HttpResponse('insert complete')


@api_view(['GET'])
def do_coloring(request):
    doc_id = request.GET.get("doc_id", "")

    doc = Statistics.objects.get(doc_id=doc_id)
    print("============doc")
    print(doc)
    gu_core_CalcifiedVSNon_calcified_data = pd.read_table(doc.filepath, index_col=0)
    df_dict = {'logFC': gu_core_CalcifiedVSNon_calcified_data["logFC"],
               'CI.L': gu_core_CalcifiedVSNon_calcified_data["CI.L"],
               'CI.R': gu_core_CalcifiedVSNon_calcified_data["CI.R"],
               'AveExpr': gu_core_CalcifiedVSNon_calcified_data["AveExpr"],
               't': gu_core_CalcifiedVSNon_calcified_data["t"],
               'P.Value': gu_core_CalcifiedVSNon_calcified_data["P.Value"],
               'adj.P.Val': gu_core_CalcifiedVSNon_calcified_data["adj.P.Val"],
               'B': gu_core_CalcifiedVSNon_calcified_data["B"]
               }
    df = pd.DataFrame(data=df_dict, columns=['logFC', 'CI.L', 'CI.R', 'AveExpr', 't', 'P.Value', 'adj.P.Val', 'B'])
    p4c.load_table_data(df)

    # todo min max绝对值中取最大，然后分别定下来左右两侧
    min_value = df['logFC'].min()
    max_value = df['logFC'].max()

    abs_min = abs(min_value)
    abs_max = abs(max_value)

    log_value = 0
    if abs_min >= abs_max:
        log_value = abs_min
    else:
        log_value = abs_max

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }

    json_color = [{
        "mappingType": "continuous",
        "mappingColumn": "logFC",
        "mappingColumnType": "Double",
        "visualProperty": "NODE_FILL_COLOR",
        "points": [{
            "value": -log_value,
            "lesser": "#2166AC",
            "equal": "#4393C3",
            "greater": "#4393C3"
        }, {
            "value": 0.0,
            "lesser": "#F7F7F7",
            "equal": "#F7F7F7",
            "greater": "#F7F7F7"
        }, {
            "value": log_value,
            "lesser": "#D6604D",
            "equal": "#D6604D",
            "greater": "#B2182B"
        }]
    }, {
        "mappingType": "passthrough",
        "mappingColumn": "MI",
        "mappingColumnType": "Double",
        "visualProperty": "EDGE_WIDTH"
    }, {
        "mappingType": "passthrough",
        "mappingColumn": "directionality",
        "mappingColumnType": "Double",
        "visualProperty": "EDGE_TARGET_ARROW_SHAPE"
    }
    ]
    # apply mapping to style
    color_res = requests.post('http://localhost:1234/v1/styles/Sample1/mappings', headers=headers, json=json_color)

    json_data = {'network': 'current'}

    response = requests.post('http://localhost:1234/v1/commands/network/get', headers=headers, json=json_data)
    suid = response.json()["data"]["SUID"]

    # apple style
    http = urllib3.PoolManager()
    r = http.request('GET', 'http://localhost:1234/v1/apply/styles/Sample1/' + str(suid))

    http = urllib3.PoolManager()
    r = http.request('GET', 'http://localhost:1234/v1/networks/' + str(suid))
    jsonData = r.json()
    nodes = jsonData["elements"]["nodes"]
    edges = jsonData["elements"]["edges"]

    http_style = urllib3.PoolManager()
    r_style = http_style.request('GET', 'http://localhost:1234/v1/styles/Sample1.json')
    json_style = r_style.json()
    style = json_style[0]["style"]

    return Response({'nodes': nodes, 'edges': edges, 'style': style})


# @api_view(['GET'])
# def get_default_style(request):
#     http = urllib3.PoolManager()
#     r = http.request('GET', 'http://localhost:1234/v1/styles/size_rank')
#     jsonData = r.json()
#     style = jsonData["defaults"]
#     return Response({'style': style})


def download1(request):
    file_path = r"static/example.svg"
    try:
        r = HttpResponse(open(file_path, "rb"))
        print(r)
        r["content_type"] = "application/octet-stream"
        r["Content-Disposition"] = "attachment;filename=pic.svg"
        return r
    except Exception:
        raise Http404("Download error")