import psycopg2

db = 'host=db dbname=postgres user=postgres password=postgres'


def connect():
    """Connect to database"""

    try:
        with psycopg2.connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT version();')
                db_version = cur.fetchone()
                print(db_version)

    except psycopg2.DatabaseError as error:
        print(error)


def create_table(name: str):
    """Create table with given name"""

    command = (
        f"""
        CREATE TABLE {name} (
        id SERIAL PRIMARY KEY,
        russian TEXT,
        english TEXT
        );"""
    )
    conn = None

    try:
        with psycopg2.connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute(command)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    finally:
        if conn is not None:
            conn.close()




def insert(values: (str, str), table: str): # TODO doesnt work
    """ Insert a new value into the table"""

    command = f"INSERT INTO {table} (russian, english) VALUES {values} RETURNING id;"

    try:
        with psycopg2.connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                word_id = cur.fetchone()[0]
                print(word_id)
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_many(values: list[(str, str),], table: str):  # TODO doesnt work
    """ Insert multiple values into the table  """

    command = f"INSERT INTO {table} (russian, english) VALUES({values})"
    conn = None
    try:
        with psycopg2.connect() as conn:
            with conn.cursor() as cur:
                cur.executemany(command)
        conn.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def update(values):
    pass


def delete(values):
    pass


def get(values):
    pass
