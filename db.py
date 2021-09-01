import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            host='db',
            database='postgres',
            user='postgres',
            password='postgres',
        )
        cur = conn.cursor()
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def create_table(name):
    pass


def save(values):
    pass


def update(values):
    pass


def delete(values):
    pass


def get(values):
    pass
