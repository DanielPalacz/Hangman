import pathmagic  # noqa Pep8 uncheck
import unittest
import sqlite3
import os
from db import initialize_db


class TestDB(unittest.TestCase):

    def test__initialize_db(self):
        """Tests if A-Sqlite3 db can be initialized."""

        # Setting up test env:
        dbname = "Test_DB.sqlite"
        if os.path.isfile(dbname):
            os.remove(dbname)
        test_conn = sqlite3.connect(dbname)
        test_cursor = test_conn.cursor()
        self.assertTrue(test_conn and test_cursor, "Setting test env failed.")

        self.assertTrue(initialize_db(test_cursor),
                        "Sqlite3 DB could not be initialized")



if __name__ == '__main__':
    unittest.main()
