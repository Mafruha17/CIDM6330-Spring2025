from django.urls import path, include
from rest_framework.routers import DefaultRouter
from mainapp.views import PatientViewSet, DeviceViewSet, ProviderViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'providers', ProviderViewSet, basename='provider')

urlpatterns = router.urls  # ✅ Correct: router provides all view patterns
