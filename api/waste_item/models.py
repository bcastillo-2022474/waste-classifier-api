from django.db import models
from core.app.waste_item.domain.entities import WasteItem as WasteItemEntity, WasteItemType
# Create your models here.

WasteItemTypes = [
    ("NON_RECYCLABLE", "non_recyclable"),
    ("RECYCLABLE", "recyclable"),
    ("ORGANIC", "organic"),
]

class WasteItem(models.Model):
    id = models.UUIDField(primary_key=True, editable=False)
    user = models.ForeignKey('authentication.User', on_delete=models.DO_NOTHING, related_name='owner_waste_items')
    image = models.UUIDField()
    material = models.CharField(max_length=255)
    type = models.CharField(max_length=255, choices=WasteItemTypes)
    approximate_weight = models.FloatField()


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('authentication.User', on_delete=models.DO_NOTHING, related_name='created_waste_items')

    @staticmethod
    def from_entity(entity: WasteItemEntity) -> "WasteItem":
        return WasteItem(
            id=entity.id,
            user_id=entity.user_id,
            image=entity.image,
            material=entity.material,
            type=entity.type,
            approximate_weight=entity.approximate_weight,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            created_by_id=entity.created_by_id
        )

    def to_entity(self) -> WasteItemEntity:
        types = dict(WasteItemTypes)

        return WasteItemEntity(
            id=self.id,
            user_id=self.user.id,
            image=self.image,
            material=self.material,
            type=WasteItemType(self.type),  # <-- convierte a Enum si es necesario
            approximate_weight=self.approximate_weight,
            created_at=self.created_at,
            updated_at=self.updated_at,
            created_by_id=self.created_by.id
        )

    def __str__(self):
        return f"WasteItem(id={self.id}, material={self.material}, type={self.get_type_display()}, weight={self.approximate_weight}kg)"
