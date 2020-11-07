import sqlite3


class DbConnection:
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except:
            print("Connection error")

        return conn


class GameDbInterface(DbConnection):

    def initialise_db(dbname: str) -> None:
        conn = GameDbInterface.create_connection(dbname)
        try:
            conn.cursor().execute("""CREATE TABLE stats (game_id INTEGER, 
            round_id INTEGER, player TEXT, guess TEXT, winner TEXT)""")
        except sqlite3.OperationalError as err:
            if err == "table stats already exists":
                pass
        conn.close()

    def take_last_game_number(dbname: str) -> int:
        conn = GameDbInterface.create_connection(dbname)
        c = conn.cursor()
        c.execute("SELECT max(game_id) FROM stats")
        game_number = c.fetchone()[0] or 0
        conn.close()
        return game_number

    def update_db(dbname: str, g_num, winner: str = None, **kw) -> None:
        conn = GameDbInterface.create_connection(dbname)
        c = conn.cursor()
        try:
            t1 = (g_num, kw["round_it"], kw["name"], kw["guess"], winner)
        except KeyError as err:
            print(err)
        if t1:
            c.execute("INSERT INTO stats VALUES (?,?,?,?,?)", t1)
            conn.commit()
        conn.close()
