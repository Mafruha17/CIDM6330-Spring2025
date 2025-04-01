from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from mainapp.api import api  # Import your Ninja API instance
#from .view import index     # Assuming you still use the index view

# 1. Simple root view
def index(request):
    return HttpResponse("Welcome to the Root Page! Try /api/patients/")

urlpatterns = [
    # 2. Root path → shows a simple welcome or instructions
    path('', index, name='root_page'),

    # 3. Django Admin
    path('admin/', admin.site.urls),

    # Django Ninja API
    path('api/', api.urls),  # <-- This replaces `include('mainapp.urls')`
   # path('api/patients/', include('mainapp.routers.patient_router'))

]
