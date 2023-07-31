"""
URL configuration for testdj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Tweet API",
        default_version='v1',
        description="Welcome to the world of Tweet",
        terms_of_service="https://www.tweet.org",
        contact=openapi.Contact(email="demo@tweet.org"),
        license=openapi.License(name="Awesome IP"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

from django.contrib import admin
from django.urls import path
from login import protein_views, cyviews, plot_views, pathTree, insert_views, networkTree

urlpatterns = [
    path('admin/', admin.site.urls),

    path('insert_proteins/', insert_views.insert_protein_data),
    # path('insert_plot/', insert_views.insert_statistics), # todo暂时好像没用上
    # path('insert_dataset/', insert_views.insert_dataset),
    path('insert_one/', insert_views.insert_one),
    path('insert_two/', insert_views.insert_two),
    path('insert_three/', insert_views.insert_three),
    path('format/', insert_views.format_file_name),
    path('get_dir/', insert_views.get_path),

    path('tree/', pathTree.path_to_dict),
    path('get_json/', pathTree.get_json_file),
    path('network_json/', networkTree.path_to_dict),
    path('get_network_json/', networkTree.get_json_file),
    path('get_diff/', networkTree.get_diff),

    path('index/', protein_views.get_protein_list, name="proteins"),
    # path('export_excel/', protein_views.export_excel, name="excel"),

    path('plot/', plot_views.get_pic_list, name="plot"),

    path('tryc/', cyviews.try_curl, name="cy"),
    path('networks/', cyviews.create_network),
    path('do_mcl/', cyviews.do_mcl),
    path('color/', cyviews.do_coloring),
    path('help/', cyviews.showHelpPage, name="help"),

    path('sidebar/', plot_views.get_child),
]
