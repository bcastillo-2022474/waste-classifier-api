from django.core.files.uploadedfile import UploadedFile
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
import json
import os

from ai_recognition_service.main import OpenAITrashClassifierService
from api.utils import get_error_status_code_from_exception
from api.waste_item.adapters import ImageScannerRepositoryImpl, WasteItemRepositoryImpl, ImageRepositoryImpl
from core.app.waste_item.application.use_cases.create_waste_item import CreateWasteItemUseCase
from core.app.waste_item.application.use_cases.scan_waste_item import ScanWasteItemUseCase
from core.app.waste_item.domain.entities import Image, WasteItemInfo, WasteItemType
from core.app.waste_item.application.use_cases.list_all_items import ListAllItemsUseCase
from rest_framework.permissions import AllowAny
from core.app.waste_item.application.use_cases.get_one_item_by_id import GetOneItemByIdUseCase
from core.app.waste_item.application.use_cases.get_all_recycling_material import GetAllRecyclingMaterialUseCase
from core.app.waste_item.application.use_cases.get_objets_recycling_material import CountMaterialAmountUseCase

class WasteItemApiView(APIView):
    parser_classes = (MultiPartParser,)

    @staticmethod
    def post(request, *args, **kwargs):
        use_case = CreateWasteItemUseCase(
            waste_item_repository=WasteItemRepositoryImpl(),
            image_repository=ImageRepositoryImpl()
        )

        try:
            image: UploadedFile = request.FILES["image"]
            data = json.loads(request.data['data'])

            waste_item = use_case.execute(
                waste_item=WasteItemInfo(
                    type=WasteItemType(data["type"]),
                    material=data["material"],
                    approximate_weight=data["approximate_weight"]
                ),
                user_id=request.user.id,
                image=Image(
                    name=image.name,
                    content=image.read(),
                    content_type=image.content_type,
                    size=image.size,
                )
            )
            return Response(waste_item)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(status=status_response, data=detail)
        
    @staticmethod
    def get(request, *args, **kwargs):
        repository = WasteItemRepositoryImpl()
        use_case = ListAllItemsUseCase(waste_item_repository=repository)
        try:
            waste_items = use_case.execute()
            paginator = PageNumberPagination()
            paginator.page_size = int(request.GET.get("page_size", 10))
            result_page = paginator.paginate_queryset(waste_items, request)
            return paginator.get_paginated_response(result_page)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(status=status_response, data=detail)



class WasteItemByIdApiView(APIView):
    @staticmethod
    def get(self, request, waste_item_id, *args, **kwargs):
        ## definicion del repo
        repository = WasteItemRepositoryImpl()
        use_case = GetOneItemByIdUseCase(waste_item_repository=repository)
        try:
            waste_item = use_case.execute(waste_item_id=waste_item_id)
            return Response(waste_item)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(status=status_response, data=detail)   
        
class StatsAllMaterialWaste(APIView):
    def get(self, request, *args, **kwargs):
        repository = WasteItemRepositoryImpl()
        use_case = GetAllRecyclingMaterialUseCase(waste_item_repository=repository)
        try:
            waste_items = use_case.execute()
            return Response(waste_items)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(status=status_response, data=detail)

class StatsMaterialWaste(APIView):
    def get(self, request, material_waste, *args, **kwargs):
        repository = WasteItemRepositoryImpl()
        use_case = CountMaterialAmountUseCase(waste_item_repository=repository)
        try:
            waste_items = use_case.execute(material_waste=material_waste)
            return Response(waste_items)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(status=status_response, data=detail)


class WasteImageScanApiView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [AllowAny]

    @staticmethod
    def post(request, *args, **kwargs):
        repository = ImageScannerRepositoryImpl(
            trash_classifier_service=OpenAITrashClassifierService(
                api_key=os.getenv("OPENAI_API_KEY"),
            )
        )
        use_case = ScanWasteItemUseCase(repository)

        try:
            image: UploadedFile = request.FILES["image"]
            waste_item = use_case.execute(image=Image(
                name=image.name,
                content=image.read(),
                content_type=image.content_type,
                size=image.size,
            ))
            return Response(waste_item)
        except Exception as e:
            status_response, detail = get_error_status_code_from_exception(e)
            return Response(status=status_response, data=detail)

