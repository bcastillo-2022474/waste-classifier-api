from django.urls import path

from api.waste_item.views import WasteImageScanApiView, WasteItemApiView

urlpatterns = [
    path("scan", WasteImageScanApiView.as_view(), name="scan-waste-item"),
    path("", WasteItemApiView.as_view(), name="crud-waste-item"),
]