from core.app.waste_item.domain.ports import WasteItemRepository
from django.http import HttpResponse

class GetExcelByUserIdUseCase:
    def __init__(self, repository: WasteItemRepository):
        self.repository = repository

    def execute(self, user_id: str) -> HttpResponse:
        return self.repository.get_excel(user_id)
