import random
from io import BytesIO
from os import getenv
from uuid import uuid4, UUID
from django.db import models 
from openpyxl import Workbook
from django.http import HttpResponse
import datetime

from core.app.waste_item.domain.ports import ImageScannerRepository, WasteItemRepository, ImageRepository
from core.app.waste_item.domain.entities import WasteItemInfo, Image, WasteItem
from waste_item.models import WasteItem as WasteItemModel
from core.app.waste_item.application.dto import StatsWasteItem
import boto3

class ImageScannerRepositoryImpl(ImageScannerRepository):
    def scan(self, image: Image) -> WasteItemInfo:
        # randomized mocked data
        possible_materials = ["plastic", "paper", "glass", "metal", "organic"]
        possible_types = ["non_recyclable", "recyclable", "organic"]

        return WasteItemInfo(
            material=random.choice(possible_materials),
            type=random.choice(possible_types),
            approximate_weight=random.uniform(0.1, 10.0)
        )

class WasteItemRepositoryImpl(WasteItemRepository):
    def create(self, waste_item: WasteItem) -> WasteItem:
        item = WasteItemModel.from_entity(entity=waste_item)
        item.save(force_insert=True)
        return item.to_entity()
    
    def list_item(self):
        return [item.to_entity() for item in WasteItemModel.objects.all()]
    
    def get(self, waste_item_id: str) -> WasteItem:
        try:
            item = WasteItemModel.objects.filter(id=waste_item_id).first()
            return item.to_entity() if item else None
        except WasteItemModel.DoesNotExist:
            raise ValueError(f"Waste item with ID {waste_item_id} not found.") 
    
    def get_material_count(self, material_waste: str) -> StatsWasteItem:
        item = (
            WasteItemModel.objects
            .filter(material=material_waste)
            .values('material')
            .annotate(count=models.Count('material'))
            .order_by('-count') 
            .first()
        )
        if item is None:
            raise ValueError(f"No waste items found for material: {material_waste}")
        return StatsWasteItem(material=item['material'], count=item['count'])

        
    def get_all_material_count(self) -> list:
        items = WasteItemModel.objects.values('material').annotate(count=models.Count('material'))
        return [StatsWasteItem(material=item['material'], count=item['count']) for item in items]

    def list_by_user_id(self, user_id: str) -> list[WasteItem]:
        items = WasteItemModel.objects.filter(user_id=user_id)
        return [item.to_entity() for item in items]
    
    
    def get_excel(self, user_id: str) -> HttpResponse:
        items = WasteItemModel.objects.filter(user_id=user_id)
        wb = Workbook()
        ws = wb.active
        ws.title = "Waste Items"

        if not items:
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=items_usuario_.xlsx'
            wb.save(response)
            return response

        exclude = {"image", "user_id", "created_by_id"}
        headers = [f.name for f in WasteItemModel._meta.fields if f.name not in exclude]
        ws.append(headers)

        for item in items:
            row = []
            for h in headers:
                value = getattr(item, h, None)
                if isinstance(value, UUID):
                    value = str(value)
                elif isinstance(value, datetime.datetime):
                    if value.tzinfo is not None:
                        value = value.replace(tzinfo=None)
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                elif value is None:
                    value = ""
                elif not isinstance(value, (str, int, float, bool)):
                    value = str(value)
                row.append(value)
            ws.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=items_usuario_.xlsx'
        wb.save(response)
        return response


class ImageRepositoryImpl(ImageRepository):
    def save(self, image: Image) -> UUID:
        # Initialize S3 client
        s3 = boto3.client(
            's3',
            endpoint_url=getenv("AWS_ENDPOINT_URL"),
            aws_access_key_id=getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=getenv("AWS_REGION")
        )

        # Upload a file
        bucket_name = getenv("AWS_BUCKET_NAME")
        image_identifier = uuid4()  # This will be the name in the S3 bucket
        file_like_object = BytesIO(image.content)

        s3.upload_fileobj(file_like_object, bucket_name, str(image_identifier), ExtraArgs={"ContentType": image.content_type})
        return image_identifier
