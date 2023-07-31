# path tree
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from login.models import Datasets, ExperimentsTypes, NetworkAndExperiment, Networks, Statistics, DocAndExperiment
import json
from django.db.models import Q
from django.core import serializers


class Node(dict):
    # initialize a node
    def __init__(self, id, text, tag, nodes=None):
        super().__init__()
        self.__dict__ = self
        self.id = id
        self.text = text
        self.tag = tag
        self.nodes = list(nodes) if nodes is not None else []

    def add_child(self, *child):
        self.nodes += child

    def show(self, layer):
        print("--" * layer + self.text)
        for c in self.nodes:
            c.show(layer + 1)


def initialize_tree():
    rootNode = Node("root", "root", "path")
    dataset = Datasets.objects.get(dataset_id="972d974a-e013-44a5-9e68-6e275f08765f")
    first_node = Node(dataset.dataset_id, dataset.name, "path")
    rootNode.add_child(first_node)
    # add second layer
    sql = "select experiment_id, pathname, path_type from experiments_types where parent_id='' and dataset_id = '" + dataset.dataset_id + "'"
    second_list = ExperimentsTypes.objects.raw(sql)
    add_child_node(second_list, first_node)
    return rootNode


# recursively add node
def add_child_node(list, node):
    networks_dict = NetworkAndExperiment.objects.values("experiment_id")
    networks_list = []
    for net in networks_dict:
        networks_list.append(net.get("experiment_id"))
    for second in list:
        if second.pathname.__contains__("Olink"):
            print("1")
        else:
            if second.path_type != "01":
                second_node = Node(second.experiment_id, second.pathname, "path")
                node.add_child(second_node)
                if second.experiment_id in networks_list:
                    obj = NetworkAndExperiment.objects.get(experiment_id=second.experiment_id)
                    network = Networks.objects.get(network_id=obj.network_id)
                    file_node = Node(network.network_id, network.filename, "network_file")
                    second_node.add_child(file_node)
                else:
                    sql = "select experiment_id, pathname, path_type from experiments_types where parent_id='" + second_node.id + "'"
                    second_list = ExperimentsTypes.objects.raw(sql)
                    add_child_node(second_list, second_node)


@staticmethod
def from_dict(dict_):
    """ Recursively (re)construct TreeNode-based tree from dictionary. """
    node = Node(dict_['id'], dict_['text'], dict_['tag'], dict_['nodes'])
    #        node.children = [TreeNode.from_dict(child) for child in node.children]
    node.children = list(map(Node.from_dict, node.children))
    return node


def path_to_dict(request):
    tree = initialize_tree()
    json_str = json.dumps(tree, indent=2)
    f2 = open('network_tree.json', 'w')
    f2.write(json_str)
    f2.close()
    return HttpResponse("success")


@api_view(['GET'])
def get_json_file(request):
    with open("network_tree.json", "r", encoding="utf-8") as f:
        content = json.load(f)
    return Response({'data': content})


def get_child(id, child_list=[]):
    ex = ExperimentsTypes.objects.get(experiment_id__exact=id)
    if ex.path_type == '01':
        child_list.append(ex.experiment_id)
    else:
        exs = ExperimentsTypes.objects.filter(parent_id=id)
        for ob in exs:
            get_child(ob.experiment_id, child_list)
    # print(child_list)
    return child_list


# todo 获取可以变颜色的file
@api_view(['GET'])
def get_diff(request):
    network_id = "74423e7e-d2ad-4103-b328-a3020fa0de9e"
    relation = NetworkAndExperiment.objects.get(network_id=network_id)
    exp = ExperimentsTypes.objects.get(experiment_id=relation.experiment_id)
    child_list = get_child(exp.experiment_id)
    doc_ids = DocAndExperiment.objects.values("doc_id").filter(experiment_id__in=child_list)

    doc_list = Statistics.objects.values('doc_id', 'filename', 'filepath').filter(Q(doc_type="03") & Q(doc_id__in=doc_ids))
    return Response({'data': doc_list})
