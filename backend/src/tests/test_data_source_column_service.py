import unittest
from src.repositories.data_source_columns_repository import DataSourceColumnRepository
from src.repositories.data_source_repository import DataSourceRepository
from src.service.data_source_service import get_data_source_service
from src.service.data_source_column_service import get_data_source_column_service
from src.schema.data_source_schema import DataSourceCreateSchema
from src.schema.data_source_column_schema import (
    DataSourceColumnCreateSchema,
    DataSourceColumnUpdateSchema,
)


class TestDataSourcColumnService(unittest.TestCase):

    def setUp(self):
        self.data_source_service = get_data_source_service(DataSourceRepository())
        self.data_source_column_service = get_data_source_column_service(
            DataSourceColumnRepository()
        )
        self.data_source_schema = DataSourceCreateSchema(
            name="Test Data Source", type="csv"  # type: ignore
        )
        self.data_source = self.data_source_service.create(self.data_source_schema)
        self.column_schema = DataSourceColumnCreateSchema(
            type="string",
            name="Test Column",
            description="Test description",
            data_source_id=self.data_source.id,
        )
        self.column = self.data_source_column_service.create(self.column_schema)

    def test_create_data_source_column(self):
        self.assertEqual(self.column.name, "Test Column")
        self.assertEqual(self.column.description, "Test description")
        self.assertEqual(self.column.data_source_id, self.data_source.id)

    def test_update_data_source_column(self):
        update_schema = DataSourceColumnUpdateSchema(
            name="Updated Column", description="Updated description"
        )
        result = self.data_source_column_service.update(self.column.id, update_schema)
        self.assertEqual(result.name, "Updated Column")
        self.assertEqual(result.description, "Updated description")

    def test_get_data_source_column_by_id(self):
        result = self.data_source_column_service.get_by_id(self.column.id)
        self.assertEqual(result.name, "Test Column")
        self.assertEqual(result.description, "Test description")

    def test_delete_data_source_column(self):
        self.data_source_column_service.delete(self.column.id)
        with self.assertRaises(
            Exception,
            msg=f"Expected NotFound error not raised by 'DataSourceService' with object id `{self.column.id}`.",
        ):
            self.data_source_column_service.get_by_id(self.column.id)

    def tearDown(self):
        self.data_source_service.delete(self.data_source.id)


if __name__ == "__main__":
    unittest.main()
