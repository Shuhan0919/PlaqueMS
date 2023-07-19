import json

from django.shortcuts import render, HttpResponse
import urllib3
import pandas as pd
import py4cytoscape as p4c
from django.views.decorators.csrf import csrf_exempt

"""
curl get one large network
"""
def try_curl(request):
    http = urllib3.PoolManager()
    # 发起一个GET请求并且获取请求的响应结果
    # r = http.request('GET', 'http://localhost:1234/v1/networks.json')
    r = http.request('GET', 'http://localhost:1234/v1/networks/155')
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



# todo import network
def create_network(request):
    gu_core_data = pd.read_table("/Users/shuhanliu/Downloads/individual_project/PlaqueMS_data/PlaqueMS_data/Networks"
                                 "/gu_core_filtered_directed_network.txt")
    edge_data = {'source': gu_core_data["Regulator"],
                 'target': gu_core_data["Target"],
                 'MI': gu_core_data["MI"],
                 'pvalue': gu_core_data["pvalue"],
                 'directionality': gu_core_data["directionality"]
                 }
    edges = pd.DataFrame(data=edge_data, columns=['source', 'target', 'MI', 'pvalue', 'directionality'])
    p4c.create_network_from_data_frames(edges=edges, title='gu_core network', collection="gu_core collection")
    # p4c.commands.commands_post('mcl cluster degreeCutoff=2 fluff=true fluffNodeDensityCutoff=0.1 haircut=true '
    #                            'includeLoops=false kCore=2 maxDepthFromStart=100 network=current nodeScoreCutoff=0.2 '
    #                            'scope=NETWORK')
    return HttpResponse('insert complete')
    # folder = 'static/PlaqueMS_data/nacl/periphery/ultrasound/_bplots_crt/'
    # filenames = os.listdir(folder)
    # filepath_prefix = '../static/PlaqueMS_data/nacl/periphery/ultrasound/_bplots_crt/'
    # for filename in filenames:
    #     id = str(uuid.uuid4())
    #     pic = models.pictures()
    #     pic.id = id
    #     pic.filename = filename
    #     pic.filepath = filepath_prefix + filename
    #     pic.pic_type = '00'
    #     pic_and_experiment = models.pic_and_experiment()
    #     second_id = str(uuid.uuid4())
    #     pic_and_experiment.id = second_id
    #     pic_and_experiment.pic_id = id
    #     pic_and_experiment.experiment_id = "3"
    #     # insert
    #     pic.save()
    #     pic_and_experiment.save()


# get networks file and Statistics file
@csrf_exempt
def file_info(request):




    return render(request, "test.html")