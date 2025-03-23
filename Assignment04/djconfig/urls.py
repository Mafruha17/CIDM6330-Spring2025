"""
URL configuration for Assignment04 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
      path('admin/', admin.site.urls),
    path('api/', include('mainapp.urls')),  # ✅ mainapp router
]
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# 1. Simple root view
def index(request):
    return HttpResponse("Welcome to the Root Page! Try /api/patients/")

urlpatterns = [
    # 2. Root path → shows a simple welcome or instructions
    path('', index, name='root_page'),

    # 3. Django Admin
    path('admin/', admin.site.urls),

    # 4. Routes all /api/ URLs to your mainapp.urls
    path('api/', include('mainapp.urls')),
]
