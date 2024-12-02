import unittest
from unittest.mock import Mock
from pg_app.api_app.utils import dao_to_dict, get_entities_as_dict
from pg_app.src.dao.base_dao import DatabaseConnectionManager


class MyTestCase(unittest.TestCase):
    def test_dao_to_dict(self):
        self.assertEqual(True, isinstance(dao_to_dict(), dict))

    def test_valid_dao(self):
        dao = Mock(spec=DatabaseConnectionManager)
        dao.configure_mock(
            get_all=Mock(
                return_value=[
                    {"id": 1, "name": "Book 1"},
                    {"id": 2, "name": "Book 2"},
                ]
            )
        )
        result = get_entities_as_dict(dao, "books")
        expected_result = {
            "books": [{"id": 1, "name": "Book 1"}, {"id": 2, "name": "Book 2"}]
        }
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
