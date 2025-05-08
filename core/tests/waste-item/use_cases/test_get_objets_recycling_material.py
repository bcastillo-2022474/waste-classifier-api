import unittest
from unittest.mock import MagicMock
from core.app.waste_item.application.use_cases.get_objets_recycling_material import CountMaterialAmountUseCase
from core.app.waste_item.domain.ports import WasteItemRepository
from core.app.waste_item.application.stats_material_dto import StatsWasteItem

import unittest
from unittest.mock import MagicMock
from core.app.waste_item.application.use_cases.get_objets_recycling_material import CountMaterialAmountUseCase
from core.app.waste_item.domain.ports import WasteItemRepository
from core.app.waste_item.application.stats_material_dto import StatsWasteItem

class TestCountMaterialAmountUseCase(unittest.TestCase):
    def setUp(self):
        # Crear un mock del repositorio
        self.mock_repository = MagicMock(spec=WasteItemRepository)
        self.use_case = CountMaterialAmountUseCase(self.mock_repository)

    def test_execute_returns_material_and_count(self):
        # Configurar el mock para devolver un objeto StatsWasteItem
        material_waste = "Plastic"
        expected_item = StatsWasteItem(material=material_waste, count=10)
        self.mock_repository.get_material_count.return_value = expected_item

        # Ejecutar el caso de uso
        result = self.use_case.execute(material_waste)

        # Verificar que el repositorio fue llamado correctamente
        self.mock_repository.get_material_count.assert_called_once_with(material_waste)

        # Verificar que el resultado sea el esperado
        self.assertEqual(result, expected_item)

    def test_execute_returns_none_when_material_not_found(self):
        # Configurar el mock para devolver None
        material_waste = "UnknownMaterial"
        self.mock_repository.get_material_count.return_value = None

        # Ejecutar el caso de uso
        result = self.use_case.execute(material_waste)

        # Verificar que el repositorio fue llamado correctamente
        self.mock_repository.get_material_count.assert_called_once_with(material_waste)

        # Verificar que el resultado sea None
        self.assertIsNone(result)

    def test_execute_raises_error_when_material_is_empty(self):
        # Ejecutar el caso de uso con un material vacío y verificar que lanza un ValueError
        with self.assertRaises(ValueError) as context:
            self.use_case.execute("")

        # Verificar el mensaje de error
        self.assertEqual(str(context.exception), "El material no puede estar vacío.")

if __name__ == "__main__":
    unittest.main()