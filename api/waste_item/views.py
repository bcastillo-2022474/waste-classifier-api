from django.core.files.uploadedfile import UploadedFile
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView


from api.utils import get_error_status_code_from_exception
from api.waste_item.adapters import ImageScannerRepositoryImpl
from core.app.waste_item.application.use_cases.scan_waste_item import ScanWasteItemUseCase
from core.app.waste_item.domain.entities import Image


# Create your views here.

class WasteImageScanApiView(APIView):
    parser_classes = (MultiPartParser,)

    @staticmethod
    def post(request, *args, **kwargs):
        repository = ImageScannerRepositoryImpl()
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

