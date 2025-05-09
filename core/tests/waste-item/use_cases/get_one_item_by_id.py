import unittest
from unittest.mock import MagicMock
from core.app.waste_item.domain.ports import WasteItemRepository
from core.app.waste_item.application.use_cases.get_one_item_by_id import GetOneItemByIdUseCase

class TestGetOneItemByIdUseCase(unittest.TestCase):
    def setUp(self):
        # Crear un mock del repositorio
        self.mock_repository = MagicMock(spec=WasteItemRepository)
        self.use_case = GetOneItemByIdUseCase(self.mock_repository)

    def test_execute_returns_item(self):
        # Configurar el mock para devolver un elemento
        waste_item_id = "123"
        expected_item = {"id": waste_item_id, "name": "Plastic Bottle"}
        self.mock_repository.get.return_value = expected_item

        # Ejecutar el caso de uso
        result = self.use_case.execute(waste_item_id)

        # Verificar que el repositorio fue llamado correctamente
        self.mock_repository.get.assert_called_once_with(waste_item_id)

        # Verificar que el resultado sea el esperado
        self.assertEqual(result, expected_item)

    def test_execute_item_not_found(self):
        # Configurar el mock para devolver None
        waste_item_id = "999"
        self.mock_repository.get.return_value = None

        # Ejecutar el caso de uso
        result = self.use_case.execute(waste_item_id)

        # Verificar que el repositorio fue llamado correctamente
        self.mock_repository.get.assert_called_once_with(waste_item_id)

        # Verificar que el resultado sea None
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()