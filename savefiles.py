import sqlite3
from os.path import join as path_join
from Rankings import ScoreboardLine

class DAO:
    def __init__(self):
        try:
            self.con = sqlite3.connect(path_join("assets", "database.db"))
            self.cur = self.con.cursor()

            build = """
            CREATE TABLE IF NOT EXISTS leaderboard
            (
                name    VARCHAR(8)  NOT NULL,
                score   INTEGER     NOT NULL,
                date    DATE        NOT NULL,
                slow    FLOAT       NOT NULL
            )
            """
            self.cur.execute(build)

            fill = """
            INSERT INTO leaderboard
            VALUES ("________", ?, "01/01/70", 0)
            """

            if len(self.get_leaderboard()) == 0:
                for n in range(1, 11):
                    self.cur.execute(fill, [n * 100000])

            self.con.commit()
        except sqlite3.Error as e:
            print(f"An error occurred during database initialization: {e}")
            if self.con:
                self.con.rollback()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_leaderboard(self):
        try:
            sql = """
            SELECT * 
            FROM leaderboard
            ORDER BY 
            leaderboard.score DESC,
            leaderboard.date ASC,
            leaderboard.slow ASC
            """
            return self.cur.execute(sql).fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while fetching the leaderboard: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def get_highscore(self):
        try:
            sql = """
            SELECT MAX(score)
            FROM leaderboard
            WHERE name <> "________"
            """
            return self.cur.execute(sql).fetchall()
        except sqlite3.Error as e:
            print(f"An error occurred while fetching the high score: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def add_to_leaderboard(self, scoreboard_line: ScoreboardLine):
        try:
            sql = """
            INSERT INTO leaderboard
            VALUES (?, ?, ?, ?) 
            """
            self.cur.execute(sql, scoreboard_line.get_values())

            sql = """
            SELECT * 
            FROM leaderboard
            ORDER BY leaderboard.score ASC, leaderboard.date DESC, leaderboard.slow DESC
            LIMIT 1;
            """
            delete_candidate = self.cur.execute(sql).fetchall()[0]

            sql = """
                DELETE FROM leaderboard
                WHERE 
                leaderboard.name = ? AND
                leaderboard.score = ? AND
                leaderboard.date = ? AND
                leaderboard.slow = ?
            """
            if len(self.get_leaderboard()) > 10:
                self.cur.execute(sql, delete_candidate)

            self.con.commit()
        except sqlite3.Error as e:
            print(f"An error occurred while adding to the leaderboard: {e}")
            if self.con:
                self.con.rollback()
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            if self.con:
                self.con.rollback()

    def close(self):
        try:
            self.con.close()
        except sqlite3.Error as e:
            print(f"An error occurred while closing the database connection: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
