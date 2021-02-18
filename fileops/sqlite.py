import sqlite3
from sqlite3 import Error, Connection


# TODO: look into SQLAlchemy
def create_connection(db_file) -> Connection:
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        raise Exception(e)
    finally:
        if conn:
            return conn


if __name__ == '__main__':
    create_connection(r"/Users/arf/PycharmProjects/UCToolbox/ucdb.db")
