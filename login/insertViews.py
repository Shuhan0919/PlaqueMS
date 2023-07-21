import json

from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from login import models
import urllib3
import uuid
import os
import pandas as pd
import csv
import numpy as np


# import zipfile
# todo unzip
# with zipfile.ZipFile('example.zip', 'r') as zip_ref:
#     zip_ref.extractall('extracted')


# insert fake data for proteins
def insert(request):
    for i in range(0, 5):
        id = str(uuid.uuid4())
        protein = models.proteins()
        protein.id = id
        protein.uniprot_id = id
        protein.protein_name = 'protein' + str(i)
        protein.gene_symbol = ''
        # insert
        protein.save()
    return HttpResponse('insert complete')


# insert data in Carotid_Plaques_Athero_Express
def insert_one(request):
    folder = 'static/PlaqueMS/Carotid_Plaques_Athero_Express/statistics/'
    filenames = os.listdir(folder)
    for filename in filenames:
        if filename != ".DS_Store":
            experiments_types = models.experiments_types()
            first_id = str(uuid.uuid4())
            experiments_types.experiment_id = first_id
            experiments_types.pathname = filename.replace("_", " ")
            experiments_types.path_type = "01"
            experiments_types.path = folder + filename
            experiments_types.parent_id = ""
            experiments_types.dataset_id = "02d22025-9c6f-46a2-8927-d813353c21d6"
            insert_bplot(folder + filename, first_id)
            # insert
            # statistics.save()
            experiments_types.save()
    return HttpResponse('insert complete')


# insert data in Carotid_Plaques_Vienna_Cohort
def insert_two(request):
    folder = 'static/PlaqueMS/Carotid_Plaques_Vienna_Cohort/'
    filenames = os.listdir(folder)
    for filename in filenames:  # guhcl
        if filename != ".DS_Store":
            experiments_types = models.experiments_types()
            first_id = str(uuid.uuid4())
            experiments_types.experiment_id = first_id
            experiments_types.pathname = filename.replace("_", " ")
            experiments_types.path_type = "00"
            experiments_types.path = folder + filename
            experiments_types.parent_id = ""
            experiments_types.dataset_id = "0581de77-69e1-4965-a9a2-0981e8435d66"
            experiments_types.save()
            second_folder = folder + filename + '/Statistics/'
            second_files = os.listdir(second_folder)
            for filename in second_files:  # core
                if filename.__contains__("vs"):
                    second = models.experiments_types()
                    second_id = str(uuid.uuid4())
                    second.experiment_id = second_id
                    second.pathname = filename.replace("_", " ")
                    second.path_type = "00"
                    second.path = second_folder + filename
                    second.parent_id = first_id
                    second.dataset_id = "0581de77-69e1-4965-a9a2-0981e8435d66"
                    second.save()
                    insert_bplot(second_folder + filename, second_id)
                elif filename != ".DS_Store":
                    second = models.experiments_types()
                    second_id = str(uuid.uuid4())
                    second.experiment_id = second_id
                    second.pathname = filename.replace("_", " ")
                    second.path_type = "00"
                    second.path = second_folder + filename
                    second.parent_id = first_id
                    second.dataset_id = "0581de77-69e1-4965-a9a2-0981e8435d66"
                    second.save()
                    third_folder = second_folder + filename + '/'
                    third_files = os.listdir(third_folder)
                    for filename in third_files:  # calcified
                        if filename.__contains__("yes_or_no"):  # yes or no
                            third = models.experiments_types()
                            third_id = str(uuid.uuid4())
                            third.experiment_id = third_id
                            third.pathname = filename.replace("_", " ")
                            third.path_type = "00"
                            third.path = third_folder + filename
                            third.parent_id = second_id
                            third.dataset_id = "0581de77-69e1-4965-a9a2-0981e8435d66"
                            third.save()
                            fourth_folder = third_folder + filename + '/'
                            fourth_files = os.listdir(fourth_folder)
                            for filename in fourth_files:
                                if filename != ".DS_Store":
                                    fourth = models.experiments_types()  # ace
                                    fourth_id = str(uuid.uuid4())
                                    fourth.experiment_id = fourth_id
                                    fourth.pathname = filename.replace("_", " ")
                                    fourth.path_type = "01"
                                    fourth.path = fourth_folder + filename
                                    fourth.parent_id = third_id
                                    fourth.dataset_id = "0581de77-69e1-4965-a9a2-0981e8435d66"
                                    fourth.save()
                                    insert_bplot(fourth_folder + filename, fourth_id)
                        elif filename != ".DS_Store":
                            third = models.experiments_types()
                            third_id = str(uuid.uuid4())
                            third.experiment_id = third_id
                            third.pathname = filename.replace("_", " ")
                            third.path_type = "00"
                            third.path = third_folder + filename
                            third.parent_id = second_id
                            third.dataset_id = "0581de77-69e1-4965-a9a2-0981e8435d66"
                            third.save()
                            insert_bplot(third_folder + filename, third_id)

            # bplotFolder = folder + filename + '/_bplots/'
            # insert_bplot(bplotFolder, first_id)

    return HttpResponse('insert complete')


# insert bplot pic
def insert_bplot(folder, experiment_id):
    # folder = 'static/PlaqueMS_data/guhcl/core/ultrasound/boxplots/'
    if os.listdir(folder).__contains__("_bplots"):
        folder = folder + '/_bplots/'
        filenames = os.listdir(folder)
        filepath_prefix = '../' + folder
        if filenames.__len__() != 0:
            for filename in filenames:
                id = str(uuid.uuid4())
                doc = models.statistics()
                doc.id = id
                doc.filename = filename
                doc.filepath = filepath_prefix + filename
                doc.doc_type = "00"
                doc_and_experiment = models.doc_and_experiment()
                second_id = str(uuid.uuid4())
                doc_and_experiment.id = second_id
                doc_and_experiment.doc_id = id
                doc_and_experiment.experiment_id = experiment_id
                # insert
                doc.save()
                doc_and_experiment.save()


fpath = "/Users/shuhanliu/Downloads/pycharmProject/testdj/static/PlaqueMS/Carotid_Plaques_Vienna_Cohort/Olink_Explore/Statistics/core/yes_or_no_for_all_medication"


def format_one(path):
    for root, dirs, files in os.walk(path):
        for filename in dirs:
            filename = os.path.join(root, filename)
            new_name = filename.replace(" ", "_")
            new_name = os.path.join(root, new_name)
            try:
                os.rename(filename, new_name)
            except Exception as e:
                print
                e
                print
                'rename dir fail\r\n'
        for filename in files:
            filename = os.path.join(root, filename)
            new_name = filename.replace(" ", "_")
            new_name = os.path.join(root, new_name)
            try:
                os.rename(filename, new_name)
            except Exception as e:
                print
                e
                print
                'rename dir fail\r\n'


def format_file_name(request):
    format_one(fpath)
    return HttpResponse('format complete')


def get_path(request):
    for root, dirs, files in os.walk(fpath):
        for dir in dirs:
            print(dir)
    return HttpResponse('dir complete')


def insertProteinData(request):
    df = pd.read_csv("static/HUMAN_9606_idmapping.dat", header=None, encoding='utf-8', delimiter="\t",
                     quoting=csv.QUOTE_NONE)
    df_uni = df.loc[df[1] == 'UniProtKB-ID']
    df_uni.columns = ['Uniprot_Accession_ID', 'UniProtKB_ID_ID', 'UniProtKB_ID']
    df_uni.set_index(df_uni['Uniprot_Accession_ID'], drop=True, append=False, inplace=False, verify_integrity=False)
    # print(df_uni.head())
    # print("===============")
    df_name = df.loc[df[1] == 'Gene_Name']
    df_name.columns = ['Uniprot_Accession_ID', 'Gene_Name_id', 'Gene_Name']
    # print(df_name.head())
    df_name.set_index(df_name['Uniprot_Accession_ID'], drop=True, append=False, inplace=False, verify_integrity=False)

    result = pd.merge(df_uni, df_name, left_on='Uniprot_Accession_ID', right_on='Uniprot_Accession_ID')
    result = result[["Uniprot_Accession_ID", "UniProtKB_ID", "Gene_Name"]]
    result["UniProtKB_ID"] = result["UniProtKB_ID"].str[:-6]
    # result.to_csv("a.csv")
    array = np.array(result)
    list = array.tolist()
    protein_list = []
    for item in list:
        protein = models.proteins()
        protein.id = str(uuid.uuid4())
        protein.uniprot_accession_id = item[0]
        protein.uniprotkb_id = item[1]
        protein.gene_name = item[2]
        protein_list.append(protein)

    models.proteins.objects.bulk_create(protein_list)
    return HttpResponse('insert proteins complete')
