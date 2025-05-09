from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from mainapp.api import api  # ✅  Ninja API instance
from dashboard.views import dashboard_view

from ai_services.api_gemini import ai_router
api.add_router("/ai/", ai_router)    # Now calls live at /api/ai/

# ✅ Simple root welcome message
def index(request):
    return HttpResponse("Welcome to the Root Page! Try /api/patients/")

urlpatterns = [
    path('', index, name='root_page'),  # ✅ Root message
    #path('', lambda req: HttpResponse("Welcome to the Root Page! Try /api/patients/")),  # optional root
    path('admin/', admin.site.urls),    # ✅ Django admin
    path('api/', api.urls),            # ✅ All API routes from Ninja
    path("dashboard/", dashboard_view, name="dashboard"),
]

