from sqlite3 import Cursor
from sqlite3 import OperationalError


sql_create_table_stats = """CREATE TABLE IF NOT EXISTS stats (
game_id INTEGER,
round_id INTEGER,
player TEXT,
guess TEXT,
winner TEXT)"""

sql_insert_into_stats = "INSERT INTO stats VALUES (?, ?,?,?,?)"


def initialize_db(c: Cursor):
    try:
        c.execute(sql_create_table_stats)
        return True
    except OperationalError as err:
        print("The issue with DB initializing happened:", err)
        return False


def get_last_game_id(c: Cursor) -> int:
    c.execute("SELECT max(game_id) FROM stats")
    game_number = c.fetchone()[0] or 0
    return game_number


def update_db(c: Cursor, g_num, winner: str = None, **kw) -> bool:
    try:
        t1 = (g_num, kw["game_round_id"], kw["name"], kw["guess"], winner)
    except KeyError as err:
        print(err)
        return False
    if t1:
        c.execute(sql_insert_into_stats, t1)
        return True


def get_all_rows(c: Cursor) -> None:
    c.execute("PRAGMA table_info(stats)")
    stats_table_columns = [x[1] for x in c.fetchall()]
    c.execute("SELECT * FROM stats")
    for row in c.fetchall():
        stats_table_columns.append(row)

    return stats_table_columns
