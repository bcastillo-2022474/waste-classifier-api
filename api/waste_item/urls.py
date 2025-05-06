from django.urls import path

from api.waste_item.views import WasteImageScanApiView, WasteItemApiView, WasteItemByIdApiView

urlpatterns = [
    path("waste-item", WasteItemApiView.as_view(), name="crud-waste-item"),
    path("waste-item/scan", WasteImageScanApiView.as_view(), name="scan-waste-item"),
    path("waste-item/<str:waste_item_id>", WasteItemByIdApiView.as_view(), name="get-waste-item-id")
]