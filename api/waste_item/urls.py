from django.urls import path

from api.waste_item.views import WasteImageScanApiView, WasteItemApiView

urlpatterns = [
    path("waste-item", WasteItemApiView.as_view(), name="crud-waste-item"),
    path("waste-item/scan", WasteImageScanApiView.as_view(), name="scan-waste-item"),
]