from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mainapp.views import PatientViewSet, DeviceViewSet, ProviderViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'providers', ProviderViewSet, basename='provider')

urlpatterns = [
    path('', include(router.urls)),  # ✅ all /api/patients, /api/devices, etc.
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
   # path('api/patients/', include('mainapp.routers.patient_router'))

]
