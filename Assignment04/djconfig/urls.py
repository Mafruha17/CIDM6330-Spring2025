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
