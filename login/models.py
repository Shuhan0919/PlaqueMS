from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
# Proteins
class Proteins(models.Model):
    id = models.CharField('id', primary_key=True, max_length=25)
    uniprot_id = models.CharField('uniprot_id', max_length=64)
    protein_name = models.CharField('protein_name', max_length=64)
    gene_symbol = models.CharField('gene_symbol', max_length=64)

    class Meta:
        db_table = 'Proteins'


class pictures(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    filename = models.CharField('filename', max_length=100)
    filepath = models.CharField('filepath', max_length=250)
    pic_type = models.CharField('pic_type', max_length=5)

    class Meta:
        db_table = 'pictures'


# todo
class networks(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    style = models.CharField('style', max_length=100)
    network = models.CharField('network', max_length=100)
    parent_id = models.CharField('parent_id', max_length=50)
    description = models.CharField('description', max_length=100)

    class Meta:
        db_table = 'networks'


# todo
class experiments(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    extraction_type = models.CharField('extraction_type', max_length=10)
    sample_type = models.CharField('sample_type', max_length=10)
    instrument = models.CharField('instrument', max_length=10)
    label = models.CharField('label', max_length=10)
    description = models.CharField('description', max_length=10)

    class Meta:
        db_table = 'experiments'


# todo
class protein_and_pic(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    uniprot_id = models.CharField('uniprot_id', max_length=50)
    pic_id = models.CharField('pic_id', max_length=50)

    class Meta:
        db_table = 'protein_and_pic'


# todo
class pic_and_experiment(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    experiment_id = models.CharField('experiment_id', max_length=50)
    pic_id = models.CharField('pic_id', max_length=50)

    class Meta:
        db_table = 'pic_and_experiment'


# todo
class network_and_experiment(models.Model):
    id = models.CharField('id', primary_key=True, max_length=50)
    experiment_id = models.CharField('experiment_id', max_length=50)
    network_id = models.CharField('network_id', max_length=50)

    class Meta:
        db_table = 'network_and_experiment'
