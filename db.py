import sqlite3


class DbConnection:
    def create_connection(db_file):
        conn = None
        try:
            conn = sqlite3.connect(db_file)
        except:
            print("Connection error")

        return conn


class DB(DbConnection):

    def initialise_db(dbname: str) -> None:
        conn = DB.create_connection(dbname)
        try:
            conn.cursor().execute("""CREATE TABLE stats (game_id INTEGER, 
            round_id INTEGER, player TEXT, guess TEXT, winner TEXT)""")
        except sqlite3.OperationalError as err:
            if err == "table stats already exists":
                pass
        conn.close()

    def get_last_game_id(dbname: str) -> int:
        conn = DB.create_connection(dbname)
        c = conn.cursor()
        c.execute("SELECT max(game_id) FROM stats")
        game_number = c.fetchone()[0] or 0
        conn.close()
        return game_number

    def update_db(dbname: str, g_num, winner: str = None, **kw) -> None:
        conn = DB.create_connection(dbname)
        c = conn.cursor()
        try:
            t1 = (g_num, kw["game_round_id"], kw["name"], kw["guess"], winner)
        except KeyError as err:
            print(err)
        if t1:
            c.execute("INSERT INTO stats VALUES (?,?,?,?,?)", t1)
            conn.commit()
        conn.close()

    def show_all_rows(dbname: str) -> None:
        conn = DB.create_connection(dbname)
        c = conn.cursor()
        c.execute("PRAGMA table_info(stats)")
        stats_table_columns = [x[1] for x in c.fetchall()]
        print(stats_table_columns)
        c.execute("SELECT * FROM stats")
        for row in c.fetchall():
            print(row)
        conn.close()
