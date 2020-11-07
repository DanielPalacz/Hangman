import sqlite3


class DbInterface:

    def initialise_db(dbname: str) -> None:
        conn = sqlite3.connect(dbname)
        try:
            conn.cursor().execute("""CREATE TABLE stats (game_id INTEGER, 
            game_round_id INTEGER, player TEXT, guess TEXT, winner TEXT)""")
        except sqlite3.OperationalError as err:
            if err == "table stats already exists":
                pass
        conn.close()

    def take_game_number(dbname: str) -> int:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        c.execute("SELECT max(rowid) FROM stats")
        game_number = c.fetchone()[0] or 0
        conn.close()
        return game_number + 1

    def update_db(dbname: str, winner: str = None, **kw) -> None:
        conn = sqlite3.connect(dbname)
        c = conn.cursor()
        g_num = DbInterface.take_game_number(dbname)
        try:
            t1 = (g_num, kw["round_it"], kw["name"], kw["guess"], winner)
        except KeyError as err:
            print(err)
        if t1:
            print(t1)
            print(*t1)
            c.execute("INSERT INTO stats VALUES (?,?,?,?,?)", t1)
            conn.commit()
        conn.close()
