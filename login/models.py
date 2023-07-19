from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
# proteins
class proteins(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    uniprot_id = models.CharField('uniprot_id', max_length=64)
    protein_name = models.CharField('protein_name', max_length=64)
    gene_symbol = models.CharField('gene_symbol', max_length=64)

    class Meta:
        db_table = 'proteins'


# class pictures(models.Model):
#     id = models.CharField('id', primary_key=True, max_length=50)
#     filename = models.CharField('filename', max_length=100, default="")
#     filepath = models.CharField('filepath', max_length=250, default="")
#     pic_type = models.CharField('pic_type', max_length=5)
#
#     class Meta:
#         db_table = 'pictures'

class datasets(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    name = models.CharField('name', max_length=100, default="")
    position = models.CharField('position', max_length=250, default="")
    description = models.CharField('description', max_length=100, null=True)

    class Meta:
        db_table = 'datasets'


# todo
class networks(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    filename = models.CharField('filename', max_length=100, default="")
    filepath = models.CharField('filepath', max_length=250, default="")
    description = models.CharField('description', max_length=100, null=True)

    class Meta:
        db_table = 'networks'


class statistics(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    filename = models.CharField('filename', max_length=100, default="")
    filepath = models.CharField('filepath', max_length=250, default="")
    doc_type = models.CharField('doc_type', max_length=5, default="")
    label = models.CharField('label', max_length=5, default="")

    class Meta:
        db_table = 'statistics'


# todo
class experiments_types(models.Model):
    experiment_id = models.CharField('id', primary_key=True, max_length=50)
    pathname = models.CharField('pathname', max_length=100)
    path_type = models.CharField('path_type', max_length=10)
    path = models.CharField('path', max_length=250)
    parent_id = models.CharField('parent_id', max_length=50)
    dataset_id = models.CharField('dataset_id', max_length=50)

    class Meta:
        db_table = 'experiments_types'


# todo
class protein_and_pic(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    uniprot_id = models.CharField('uniprot_id', max_length=50)
    pic_id = models.CharField('pic_id', max_length=50)

    class Meta:
        db_table = 'protein_and_pic'


# todo
class doc_and_experiment(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    experiment_id = models.CharField('experiment_id', max_length=50)
    doc_id = models.CharField('doc_id', max_length=50)

    class Meta:
        db_table = 'doc_and_experiment'


# todo
class network_and_experiment(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    experiment_id = models.CharField('experiment_id', max_length=50)
    network_id = models.CharField('network_id', max_length=50)

    class Meta:
        db_table = 'network_and_experiment'
