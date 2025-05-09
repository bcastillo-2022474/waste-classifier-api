from django.urls import path

from api.waste_item.views import WasteImageScanApiView, WasteItemApiView, WasteItemByIdApiView, StatsAllMaterialWaste, StatsMaterialWaste

urlpatterns = [
    path("waste-item", WasteItemApiView.as_view(), name="crud-waste-item"),
    path("waste-item/scan", WasteImageScanApiView.as_view(), name="scan-waste-item"),
    path("waste-item/<str:waste_item_id>", WasteItemByIdApiView.as_view(), name="get-waste-item-id"),
    path("waste-item/stats", StatsAllMaterialWaste.as_view(), name="stats-waste-item"),
    path("waste-item/stats/<str:material_waste>", StatsMaterialWaste.as_view(), name="stats-waste-item-material"),
]