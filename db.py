import psycopg2
from main import logger


db = 'host=db dbname=postgres user=postgres password=postgres'


def connect():
    """Connect to database"""

    try:
        with psycopg2.connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT version();')
                db_version = cur.fetchone()
                logger.info(db_version)

    except psycopg2.DatabaseError as error:
        logger.error(error)


def create_table(name: str):
    """Create table with given name"""

    command = (
        f"""
        CREATE TABLE {name} (
        id SERIAL PRIMARY KEY,
        channel TEXT,
        pattern TEXT
        );"""
    )
    conn = None

    try:
        with psycopg2.connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute(command)

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)

    finally:
        if conn is not None:
            conn.close()


def insert(channel: str, pattern: str, table: str): # TODO doesnt work
    """ Insert a new value into the table"""

    command = f"INSERT INTO {table} (channel, pattern) VALUES {(channel, pattern)} RETURNING id;"

    try:
        with psycopg2.connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                word_id = cur.fetchone()[0]
                logger.info(word_id)
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)


def update(values):
    pass


def delete(values):
    pass


def get(values):
    pass
