import unittest
from pydantic_core import ValidationError
from src.repositories.data_source_repository import DataSourceRepository
from src.schema.data_source_schema import DataSourceCreateSchema, DataSourceUpdateSchema
from src.service.data_source_service import get_data_source_service


class TestDataSourceService(unittest.TestCase):

    def setUp(self):
        self.data_source_service = get_data_source_service(DataSourceRepository())
        self.data_source_create_schema = DataSourceCreateSchema(
            name="Test Data Source", type="csv"  # type: ignore
        )
        self.created_data_source = self.data_source_service.create(
            self.data_source_create_schema
        )

    def test_create_data_source(self):

        self.assertIsNotNone(self.created_data_source.id)
        self.assertEqual(self.created_data_source.name, "Test Data Source")
        self.assertEqual(self.created_data_source.type, "csv")

    def test_get_by_id_data_source(self):
        got = self.data_source_service.get_by_id(self.created_data_source.id)
        self.assertEqual(got.id, got.id)

    def test_update_data_source(self):
        update_schema = DataSourceUpdateSchema(name="Updated Data Source", type="csv")  # type: ignore
        result = self.data_source_service.update(
            self.created_data_source.id, update_schema
        )
        self.assertEqual(result.name, "Updated Data Source")
        self.assertEqual(result.type, "csv")

    def test_create_data_source_with_invalid_schema(self):
        with self.assertRaises(ValidationError):
            data_source_schema = DataSourceCreateSchema(name=None, type="csv")  # type: ignore
            self.data_source_service.create(data_source_schema)

    def tearDown(self):
        self.data_source_service.delete(self.created_data_source.id)


if __name__ == "__main__":
    unittest.main()
