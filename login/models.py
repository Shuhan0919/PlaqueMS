from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
# Proteins
class Proteins(models.Model):
    id = models.CharField('id', primary_key=True, max_length=25)
    uniprot_id = models.CharField('uniprot_id',max_length=64)
    protein_name = models.CharField('protein_name',max_length=64)
    gene_symbol = models.CharField('gene_symbol',max_length=64)

    class Meta:
        db_table = 'Proteins'

class pictures(models.Model):
    id = models.CharField('id', primary_key=True, max_length=25)
    filename = models.CharField('filename',max_length=100)
    filepath = models.CharField('filepath',max_length=250)
    pic_type = models.CharField('pic_type',max_length=5)

    class Meta:
        db_table = 'pictures'
# Statistics
# class Statistics(models.Model):
#     id = models.CharField('id', primary_key=True, max_length=25)
#     name = models.CharField(max_length=64)
#     type = models.CharField(max_length=64)
#     desc = models.CharField(max_length=64)

    # class Meta:
    #     db_table = 'Proteins'
# PPI
# class PPI(models.Model):
#     id = models.CharField('id', primary_key=True, max_length=25)
#     name = models.CharField(max_length=64)
#     type = models.CharField(max_length=64)
#     desc = models.CharField(max_length=64)

    # class Meta:
    #     db_table = 'Proteins'
# Experiments
# class Experiments(models.Model):
#     id = models.CharField('id', primary_key=True, max_length=25)
#     name = models.CharField(max_length=64)
#     type = models.CharField(max_length=64)
#     desc = models.CharField(max_length=64)

    # class Meta:
    #     db_table = 'Proteins'
# Phenotypes
# class Phenotypes(models.Model):
#     id = models.CharField('id', primary_key=True, max_length=25)
#     name = models.CharField(max_length=64)
#     type = models.CharField(max_length=64)
#     desc = models.CharField(max_length=64)

    # class Meta:
    #     db_table = 'Proteins'