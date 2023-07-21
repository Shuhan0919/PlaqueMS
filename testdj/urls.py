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
from django.urls import path, include, re_path
from login import views
from login import cyviews
from login import insertViews
from login import pathTree

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.show_list, name="proteins"),
    path('insertOne/', insertViews.insert_one),
    path('insertTwo/', insertViews.insert_two),
    path('plot/', views.pic_info, name="plot"),

    path('format/', insertViews.format_file_name),
    path('get_dir/', insertViews.get_path),
    path('tree/', pathTree.path_to_dict),
    path('get_json/', pathTree.get_json_file),

    path('tryc/', cyviews.try_curl, name="cy"),
    path('tryc2/', cyviews.try_curl2),
    path('networks/', cyviews.create_network),
    path('do_mcl/', cyviews.do_mcl),
    path('color/', cyviews.do_coloring),
    path('insert_proteins/', insertViews.insertProteinData),
    # re_path(r'^doc(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # path('doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
