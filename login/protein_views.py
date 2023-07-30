from django.http import HttpResponse, Http404
from django.shortcuts import render

from login.models import Proteins
from django.db.models import Q

import xlwt
from io import BytesIO

"""
get proteins
"""


def get_protein_list(request):
    # get keywords
    uniprotkb_id = request.GET.get("uniprotkb_id", "")
    gene_name = request.GET.get("gene_name", "")
    page_number = request.GET.get("page_number", "")

    if page_number:
        current_page = int(page_number)
    else:
        current_page = 1
    page_size = 10

    query = Proteins.objects

    if gene_name and uniprotkb_id:
        name_search_list = gene_name.split(",")
        id_search_list = uniprotkb_id.split(",")
        query = query.filter(Q(uniprotkb_id__in=id_search_list) | Q(gene_name__in=name_search_list))

    elif uniprotkb_id and gene_name == '':
        id_search_list = uniprotkb_id.split(",")
        query = query.filter(uniprotkb_id__in=id_search_list)

    elif uniprotkb_id == '' and gene_name:
        name_search_list = gene_name.split(",")
        query = query.filter(gene_name__in=name_search_list)

    start_row = (current_page - 1) * page_size
    end_row = current_page * page_size

    result = query.values('protein_id', 'uniprot_accession_id', 'uniprotkb_id', 'gene_name')[start_row:end_row]

    counts = query.count()

    total_count = 0
    if counts % page_size == 0:
        total_count = counts // page_size
    else:
        total_count = counts // page_size + 1

    if current_page > 1:
        has_previous = True
        previous_page = current_page - 1
    else:
        has_previous = False
        previous_page = current_page

    if current_page < total_count:
        has_next = True
        next_page = current_page + 1
    else:
        has_next = False
        next_page = current_page
    context = {
        "result": result,
        "page": current_page,
        "gene_name": gene_name,
        "uniprotkb_id": uniprotkb_id,
        "total_count": total_count,
        "has_previous": has_previous,
        "has_next": has_next,
        "previous_page": previous_page,
        "next_page": next_page,
    }
    return render(request, "protein.html", context)


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


# 导出excel数据
# def export_excel(request):
#     # 设置HTTPResponse的类型
#     response = HttpResponse(content_type='application/vnd.ms-excel')
#     response['Content-Disposition'] = 'attachment;filename=order.xls'
#     # 创建一个文件对象
#     wb = xlwt.Workbook(encoding='utf8')
#     # 创建一个sheet对象
#     sheet = wb.add_sheet('order-sheet')
#
#     # 设置文件头的样式,这个不是必须的可以根据自己的需求进行更改
#     style_heading = xlwt.easyxf("""
#             font:
#                 name Arial,
#                 colour_index white,
#                 bold on,
#                 height 0xA0;
#             align:
#                 wrap off,
#                 vert center,
#                 horiz center;
#             pattern:
#                 pattern solid,
#                 fore-colour 0x19;
#             borders:
#                 left THIN,
#                 right THIN,
#                 top THIN,
#                 bottom THIN;
#             """)
#
#     # 写入文件标题
#     sheet.write(0, 0, 'uniprot_accession_id', style_heading)
#     sheet.write(0, 1, 'uniprotkb_id', style_heading)
#     sheet.write(0, 2, 'gene_name', style_heading)
#
#     # 写入数据
#     data_row = 1
#     for i in Proteins.objects.all():
#         sheet.write(data_row, 0, i.uniprot_accession_id)
#         sheet.write(data_row, 1, i.uniprotkb_id)
#         sheet.write(data_row, 2, i.gene_name)
#         data_row = data_row + 1
#
#     # 写出到IO
#     output = BytesIO()
#     wb.save(output)
#     # 重新定位到开始
#     output.seek(0)
#     response.write(output.getvalue())
#
#     # 说明：需要写入的是二维列表target_data
#     # 将数据写入excel表格
#     workbook = xlwt.Workbook()
#     sheet1 = workbook.add_sheet("Sheet1")
#     sheet2 = workbook.add_sheet("Sheet2")
#     sheet3 = workbook.add_sheet("Sheet3")
#     al = xlwt.Alignment()
#     al.horz = 0x02  # 设置水平居中
#     # 创建样式对象，初始化样式
#     style = xlwt.XFStyle()
#     style.alignment = al  # 设置水平居中
#
#     print(len(target_data))  # 看target_data数据长度，通过查看其实有 14W 行，所以我们拆成了3个sheet
#
#     for i in range(0, 50000):
#         for j in range(0, len(target_data[i])):
#             sheet1.write(i, j, target_data[i][j], style)
#
#     for i in range(50000, 100000):
#         for j in range(0, len(target_data[i])):
#             sheet2.write(i - 50000, j, target_data[i][j], style)
#
#     for i in range(100000, len(target_data)):
#         for j in range(0, len(target_data[i])):
#             sheet3.write(i - 100000, j, target_data[i][j], style)
#
#     workbook.save("target_data1220.xls")  # 保存到target_data.xls
#
#     return response


