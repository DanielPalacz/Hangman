import pathmagic  # noqa Pep8 uncheck
import unittest
import sqlite3
import os
from db import initialize_db


class TestDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Class level fixture"""
        # Setting up test env:
        cls._dbname = "Test_DB.sqlite"
        if os.path.isfile(cls._dbname):
            os.remove(cls._dbname)

        cls._conn = sqlite3.connect(cls._dbname)
        cls._cursor = cls._conn.cursor()
        cls._stats_table_defined = {"game_id": "INTEGER",
                                    "round_id": "INTEGER",
                                    "player": "TEXT",
                                    "guess": "TEXT",
                                    "winner": "TEXT"}

    def setUp(self):
        """Test level fixture"""
        pass

    def test__initialize_db1(self):
        # 1st line of Docstring goes to verbose mode ... (-v)
        """
        Tests if A-Sqlite3 db can be initialized."""
        initialize_db(TestDB._cursor)
        TestDB._conn.commit()
        self.assertTrue(os.path.isfile(TestDB._dbname), "DB was not created.")

    def test__initialize_db2(self):
        """
        ...
        """
        TestDB._cursor.execute("PRAGMA table_info(stats)")
        test_stats = {x[1]: x[2] for x in TestDB._cursor.fetchall()}
        for y in TestDB._stats_table_defined.keys():
            with self.subTest(y):
                self.assertEqual(TestDB._stats_table_defined[y], test_stats[y],
                                 "column definition doesnt match with setup")

    def tearDown(self):
        """Test level fixture"""
        pass

    @classmethod
    def tearDownClass(cls):
        """Class level fixture"""
        cls._conn.close()


def setUpModule():
    """Module level fixture"""
    print("")
    mod_name = "'" + __name__ + "'"
    print("Tests for module:", mod_name, "are starting.\n")


def tearDownModule():
    """Module level fixture"""
    print("")
    print("End of Tests for module:", __name__)


if __name__ == '__main__':
    unittest.main()
