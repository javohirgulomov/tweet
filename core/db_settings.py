import psycopg2
from psycopg2.extras import DictCursor

from core.config import DB_CONFIG


class DatabaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.cursor = self.conn.cursor(cursor_factory=DictCursor)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()

        if self.conn:
            self.conn.close()

        if self.cursor:
            self.cursor.close()

    def execute(self, query, params):
        self.cursor.execute(query, params)

    def fetchone(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def fetchall(self, query, params):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()


def execute_query(query, params=None, fetch=None):
    try:
        with DatabaseManager() as db:
            if fetch == "one":
                return db.fetchone(query=query, params=params)
            elif fetch == "all":
                return db.fetchall(query=query, params=params)
            else:
                db.execute(query=query, params=params)
                return True
    except psycopg2.Error as e:
        print(e)
        return None
