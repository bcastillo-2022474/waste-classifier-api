from django.urls import path

from .views import WasteImageScanApiView

urlpatterns = [
    path("scan", WasteImageScanApiView.as_view(), name="scan-waste-item"),
]