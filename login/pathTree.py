# path tree
from django.http import HttpResponse

from login import models
import json


class Node(dict):
    # initialize a node
    def __init__(self, id, name, children=None):
        super().__init__()
        self.__dict__ = self
        self.id = id
        self.name = name
        self.children = list(children) if children is not None else []

    def add_child(self, *child):
        self.children += child

    def show(self, layer):
        print("--" * layer + self.name)
        for c in self.children:
            c.show(layer + 1)


def initialize_tree():
    rootNode = Node("root", "root")
    dataset_list = models.datasets.objects.all()
    for dataset in dataset_list:
        first_node = Node(dataset.id, dataset.name)
        rootNode.add_child(first_node)
        # add second layer
        sql = "select experiment_id, pathname, path_type from experiments_types where parent_id='' and dataset_id = '" + dataset.id + "'"
        second_list = models.experiments_types.objects.raw(sql)
        add_child_node(second_list, first_node)
    return rootNode
    #
    # root.show(0)
    # return HttpResponse("initialize_tree")


# recursively add node
def add_child_node(list, node):
    for second in list:
        if second.path_type == "01":
            second_node = Node(second.experiment_id, second.pathname)
            node.add_child(second_node)
        elif second.path_type == "00":
            second_node = Node(second.experiment_id, second.pathname)
            node.add_child(second_node)
            sql = "select experiment_id, pathname, path_type from experiments_types where parent_id='" + second_node.id + "'"
            second_list = models.experiments_types.objects.raw(sql)
            add_child_node(second_list, second_node)


import os
import json


# def path_to_dict():
#     item = os.path.basename(path)
#     d = {'name': item, 'children': [path_to_dict(os.path.join(path, x)) for x in os.listdir(path) if
#                                     os.path.isdir(os.path.join(path, x)) and os.path.basename(os.path.join(path, x))[
#                                         0] not in ["~", "."]]}
#     return d
# node2 = json.dumps(path_to_dict(path))
# f2 = open('json_tree.json', 'w')
# f2.write(node2)
# f2.close()


@staticmethod
def from_dict(dict_):
    """ Recursively (re)construct TreeNode-based tree from dictionary. """
    node = Node(dict_['id'], dict_['name'], dict_['children'])
    #        node.children = [TreeNode.from_dict(child) for child in node.children]
    node.children = list(map(Node.from_dict, node.children))
    return node


def path_to_dict(request):
    tree = initialize_tree()
    json_str = json.dumps(tree, indent=2)
    print(json_str)
    f2 = open('json_tree.json', 'w')
    f2.write(json_str)
    f2.close()
    return HttpResponse("success")
