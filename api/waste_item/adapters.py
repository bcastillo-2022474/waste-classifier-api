import random
from io import BytesIO
from os import getenv
from uuid import uuid4, UUID
from django.db import models

from core.app.waste_item.domain.ports import ImageScannerRepository, WasteItemRepository, ImageRepository
from core.app.waste_item.domain.entities import WasteItemInfo, Image, WasteItem
from waste_item.models import WasteItem as WasteItemModel
from core.app.waste_item.application.dto import StatsWasteItem
import boto3
import base64

from ai_recognition_service.main import OpenAITrashClassifierService


class ImageScannerRepositoryImpl(ImageScannerRepository):
    def __init__(self, trash_classifier_service: OpenAITrashClassifierService):
        self._trash_classifier_service = trash_classifier_service

    def scan(self, image: Image) -> WasteItemInfo:
        # randomized mocked data
        response_data = self._trash_classifier_service.analyze_waste_image(
            base64_image=base64.b64encode(image.content).decode('utf-8')
        )

        print(response_data)

        if not response_data["success"]:
            raise ValueError("Image analysis failed")

        item_info = response_data["classification"]

        return WasteItemInfo(
            material=item_info['material'],
            type=item_info['type'],
            approximate_weight=item_info['approximate_weight']
        )


class WasteItemRepositoryImpl(WasteItemRepository):
    def create(self, waste_item: WasteItem) -> WasteItem:
        item = WasteItemModel.from_entity(entity=waste_item)
        item.save(force_insert=True)
        return item.to_entity()

    def list(self):
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

        s3.upload_fileobj(file_like_object, bucket_name, str(image_identifier),
                          ExtraArgs={"ContentType": image.content_type})
        return image_identifier
