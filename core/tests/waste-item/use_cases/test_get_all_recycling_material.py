import unittest
from unittest.mock import MagicMock
from core.app.waste_item.application.use_cases.get_all_recycling_material import GetAllRecyclingMaterialUseCase
from core.app.waste_item.domain.ports import WasteItemRepository
from core.app.waste_item.application.dto import StatsWasteItem

class TestGetAllRecyclingMaterialUseCase(unittest.TestCase):
    def setUp(self):
        # Crear un mock del repositorio
        self.mock_repository = MagicMock(spec=WasteItemRepository)
        self.use_case = GetAllRecyclingMaterialUseCase(self.mock_repository)

    def test_execute_returns_all_material_counts(self):
        # Configurar el mock para devolver una lista de StatsWasteItem
        expected_data = [
            StatsWasteItem(material="Plastic", count=10),
            StatsWasteItem(material="Glass", count=5),
            StatsWasteItem(material="Metal", count=8),
        ]
        self.mock_repository.get_all_material_count.return_value = expected_data

        # Ejecutar el caso de uso
        result = self.use_case.execute()

        # Verificar que el repositorio fue llamado correctamente
        self.mock_repository.get_all_material_count.assert_called_once()

        # Verificar que el resultado sea el esperado
        self.assertEqual(result, expected_data)

    def test_execute_returns_empty_list_when_no_data(self):
        # Configurar el mock para devolver una lista vacía
        self.mock_repository.get_all_material_count.return_value = []

        # Ejecutar el caso de uso
        result = self.use_case.execute()

        # Verificar que el repositorio fue llamado correctamente
        self.mock_repository.get_all_material_count.assert_called_once()

        # Verificar que el resultado sea una lista vacía
        self.assertEqual(result, [])

if __name__ == "__main__":
    unittest.main()