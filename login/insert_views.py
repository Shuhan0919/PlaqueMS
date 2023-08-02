from django.shortcuts import HttpResponse
from login.models import Proteins, Datasets, Statistics, ExperimentsTypes, DocAndExperiment, Networks, \
    NetworkAndExperiment
import os
import pandas as pd
import csv
import numpy as np
import uuid


def insert_protein_data(request):
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
    # result["UniProtKB_ID"] = result["UniProtKB_ID"].str[:-6]
    # result.to_csv("a.csv")
    array = np.array(result)
    list = array.tolist()
    protein_list = []
    for item in list:
        protein = Proteins()
        protein.protein_id = str(uuid.uuid4())
        protein.uniprot_accession_id = item[0]
        protein.uniprotkb_id = item[1]
        protein.gene_name = item[2]
        protein_list.append(protein)

    Proteins.objects.bulk_create(protein_list)
    return HttpResponse('insert proteins complete')


# import zipfile
# todo unzip
# with zipfile.ZipFile('example.zip', 'r') as zip_ref:
#     zip_ref.extractall('extracted')

def insert_dataset(request):
    folder = 'static/PlaqueMS/'
    filenames = os.listdir(folder)
    for filename in filenames:
        if filename != ".DS_Store":
            id = str(uuid.uuid4())
            dataset = Datasets()
            dataset.dataset_id = id
            dataset.name = filename.replace("_", " ")
            dataset.position = ''
            dataset.description = ''
            dataset.save()
    return HttpResponse('insert dataset complete')


# insert data in Carotid_Plaques_Athero_Express
def insert_one(request):
    folder = 'static/PlaqueMS/Carotid_Plaques_Athero_Express/statistics/'
    filenames = os.listdir(folder)
    for filename in filenames:
        if filename != ".DS_Store":
            experiments_types = ExperimentsTypes()
            first_id = str(uuid.uuid4())
            experiments_types.experiment_id = first_id
            experiments_types.pathname = filename.replace("_", " ")
            experiments_types.path_type = "01"
            experiments_types.path = folder + filename
            experiments_types.parent_id = ""
            experiments_types.dataset_id = "42d1dde2-188f-4b71-9db2-57148376abea"
            insert_bplot(folder + filename, first_id)
            insert_statistics(folder + filename, first_id)
            experiments_types.save()
    return HttpResponse('insert complete')


# insert data in Carotid_Plaques_Vienna_Cohort
def insert_two(request):
    folder = 'static/PlaqueMS/Carotid_Plaques_Vienna_Cohort/'
    filenames = os.listdir(folder)
    for filename in filenames:  # guhcl
        if filename != ".DS_Store":
            experiments_types = ExperimentsTypes()
            first_id = str(uuid.uuid4())
            experiments_types.experiment_id = first_id
            experiments_types.pathname = filename.replace("_", " ")
            experiments_types.path_type = "00"
            experiments_types.path = folder + filename
            experiments_types.parent_id = ""
            experiments_types.dataset_id = "972d974a-e013-44a5-9e68-6e275f08765f"
            experiments_types.save()
            second_folder = folder + filename + '/Statistics/'
            second_files = os.listdir(second_folder)
            for filename in second_files:  # core
                if filename.__contains__("vs"):
                    second = ExperimentsTypes()
                    second_id = str(uuid.uuid4())
                    second.experiment_id = second_id
                    second.pathname = filename.replace("_", " ")
                    second.path_type = "01"
                    second.path = second_folder + filename
                    second.parent_id = first_id
                    second.dataset_id = "972d974a-e013-44a5-9e68-6e275f08765f"
                    second.save()
                    insert_bplot(second_folder + filename, second_id)
                    insert_statistics(second_folder + filename, second_id)
                elif filename != ".DS_Store":
                    second = ExperimentsTypes()
                    second_id = str(uuid.uuid4())
                    second.experiment_id = second_id
                    second.pathname = filename.replace("_", " ")
                    second.path_type = "00"
                    second.path = second_folder + filename
                    second.parent_id = first_id
                    second.dataset_id = "972d974a-e013-44a5-9e68-6e275f08765f"
                    second.save()
                    third_folder = second_folder + filename + '/'
                    third_files = os.listdir(third_folder)
                    for filename in third_files:  # calcified
                        if filename.__contains__("network"):
                            insert_network(third_folder, filename, second_id)
                        elif filename.__contains__("yes_or_no"):  # yes or no
                            third = ExperimentsTypes()
                            third_id = str(uuid.uuid4())
                            third.experiment_id = third_id
                            third.pathname = filename.replace("_", " ")
                            third.path_type = "00"
                            third.path = third_folder + filename
                            third.parent_id = second_id
                            third.dataset_id = "972d974a-e013-44a5-9e68-6e275f08765f"
                            third.save()
                            fourth_folder = third_folder + filename + '/'
                            fourth_files = os.listdir(fourth_folder)
                            for filename in fourth_files:
                                if filename != ".DS_Store":
                                    fourth = ExperimentsTypes()  # ace
                                    fourth_id = str(uuid.uuid4())
                                    fourth.experiment_id = fourth_id
                                    fourth.pathname = filename.replace("_", " ")
                                    fourth.path_type = "01"
                                    fourth.path = fourth_folder + filename
                                    fourth.parent_id = third_id
                                    fourth.dataset_id = "972d974a-e013-44a5-9e68-6e275f08765f"
                                    fourth.save()
                                    insert_bplot(fourth_folder + filename, fourth_id)
                                    insert_statistics(fourth_folder + filename, fourth_id)
                        elif filename != ".DS_Store":
                            third = ExperimentsTypes()
                            third_id = str(uuid.uuid4())
                            third.experiment_id = third_id
                            third.pathname = filename.replace("_", " ")
                            third.path_type = "01"
                            third.path = third_folder + filename
                            third.parent_id = second_id
                            third.dataset_id = "972d974a-e013-44a5-9e68-6e275f08765f"
                            third.save()
                            insert_bplot(third_folder + filename, third_id)
                            insert_statistics(third_folder + filename, third_id)
    return HttpResponse('insert complete')


# insert data in Coronary_Arteries_University_of_Virginia_Cohort
def insert_three(request):
    folder = 'static/PlaqueMS/Coronary_Arteries_University_of_Virginia_Cohort/statistics/'
    filenames = os.listdir(folder)
    for filename in filenames:  # guhcl
        if filename.__contains__("in_segments"):
            experiments_types = ExperimentsTypes()
            first_id = str(uuid.uuid4())
            experiments_types.experiment_id = first_id
            experiments_types.pathname = filename.replace("_", " ")
            experiments_types.path_type = "00"
            experiments_types.path = folder + filename
            experiments_types.parent_id = ""
            experiments_types.dataset_id = "3542c8b3-224b-41ae-8598-a9eeed0f8eb0"
            experiments_types.save()
            second_folder = folder + filename + '/'
            second_files = os.listdir(second_folder)
            for filename in second_files:  # core
                if filename != ".DS_Store":
                    second = ExperimentsTypes()
                    second_id = str(uuid.uuid4())
                    second.experiment_id = second_id
                    second.pathname = filename.replace("_", " ")
                    second.path_type = "01"
                    second.path = second_folder + filename
                    second.parent_id = first_id
                    second.dataset_id = "3542c8b3-224b-41ae-8598-a9eeed0f8eb0"
                    second.save()
                    insert_bplot(second_folder + filename, second_id)
                    insert_statistics(second_folder + filename, second_id)
        elif filename != ".DS_Store":
            experiments_types = ExperimentsTypes()
            first_id = str(uuid.uuid4())
            experiments_types.experiment_id = first_id
            experiments_types.pathname = filename.replace("_", " ")
            experiments_types.path_type = "01"
            experiments_types.path = folder + filename
            experiments_types.parent_id = ""
            experiments_types.dataset_id = "3542c8b3-224b-41ae-8598-a9eeed0f8eb0"
            experiments_types.save()
            insert_bplot(folder + filename, first_id)
            insert_statistics(folder + filename, first_id)
    return HttpResponse('insert complete')


# insert bplot pic
def insert_bplot(folder, experiment_id):
    if os.listdir(folder).__contains__("_bplots"):
        folder = folder + '/_bplots/'
        filenames = os.listdir(folder)
        filepath_prefix = '../' + folder
        if filenames.__len__() != 0:
            for filename in filenames:
                id = str(uuid.uuid4())
                doc = Statistics()
                doc.doc_id = id
                doc.filename = filename
                doc.filepath = filepath_prefix + filename
                doc.doc_type = "00"
                doc_and_experiment = DocAndExperiment()
                second_id = str(uuid.uuid4())
                doc_and_experiment.id = second_id
                doc_and_experiment.doc_id = id
                doc_and_experiment.experiment_id = experiment_id
                # insert
                doc.save()
                doc_and_experiment.save()


def insert_statistics(folder, experiment_id):
    folder = folder + '/'
    filenames = os.listdir(folder)
    filepath_prefix = '../' + folder
    for filename in filenames:
        if filename.__contains__("heatmap"):
            id = str(uuid.uuid4())
            doc = Statistics()
            doc.doc_id = id
            doc.filename = filename
            doc.filepath = filepath_prefix + filename
            doc.doc_type = "02"
            doc_and_experiment = DocAndExperiment()
            second_id = str(uuid.uuid4())
            doc_and_experiment.id = second_id
            doc_and_experiment.doc_id = id
            doc_and_experiment.experiment_id = experiment_id
            doc.save()
            doc_and_experiment.save()
        elif filename.__contains__("volcano"):
            id = str(uuid.uuid4())
            doc = Statistics()
            doc.doc_id = id
            doc.filename = filename
            doc.filepath = filepath_prefix + filename
            doc.doc_type = "01"
            if filename.__contains__("unlabeled"):
                doc.label = '00'
            else:
                doc.label = '01'
            doc_and_experiment = DocAndExperiment()
            second_id = str(uuid.uuid4())
            doc_and_experiment.id = second_id
            doc_and_experiment.doc_id = id
            doc_and_experiment.experiment_id = experiment_id
            doc.save()
            doc_and_experiment.save()
        elif filename.__contains__("diff_exp"):
            id = str(uuid.uuid4())
            doc = Statistics()
            doc.doc_id = id
            doc.filename = filename
            doc.filepath = folder + filename
            doc.doc_type = "03"
            doc_and_experiment = DocAndExperiment()
            second_id = str(uuid.uuid4())
            doc_and_experiment.id = second_id
            doc_and_experiment.doc_id = id
            doc_and_experiment.experiment_id = experiment_id
            doc.save()
            doc_and_experiment.save()
    return HttpResponse('insert complete')


def insert_network(folder, filename, experiment_id):
    id = str(uuid.uuid4())
    network = Networks()
    network.network_id = id
    network.filename = filename
    network.filepath = folder + filename
    network_and_experiment = NetworkAndExperiment()
    second_id = str(uuid.uuid4())
    network_and_experiment.id = second_id
    network_and_experiment.network_id = id
    network_and_experiment.experiment_id = experiment_id
    # insert
    network.save()
    network_and_experiment.save()


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


def insert_diff(folder, filename, experiment_id):
    id = str(uuid.uuid4())
    network = Networks()
    network.network_id = id
    network.filename = filename
    network.filepath = folder + filename
    network_and_experiment = NetworkAndExperiment()
    second_id = str(uuid.uuid4())
    network_and_experiment.id = second_id
    network_and_experiment.network_id = id
    network_and_experiment.experiment_id = experiment_id
    # insert
    network.save()
    network_and_experiment.save()