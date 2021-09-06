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


def insert(channel: str, pattern: str, table: str):
    """ Insert a new value into the table"""

    command = f"INSERT INTO {table} (channel, pattern) VALUES {(channel, pattern)} RETURNING id;"

    if not is_table(table):  # Throws error
        logger.info('no table')
        create_table(table)

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


def get(table):
    """Return a string with all user's subs"""

    if not is_table(table):
        return "You don't have any subscriptions yet"

    command = f"SELECT * FROM {table}"

    with psycopg2.connect(db) as conn:
        with conn.cursor() as cur:
            cur.execute(command)
            list_of_subs = cur.fetchone()

    result = str(
        [f'{channel} - {pattern}\n' for channel, pattern in list_of_subs]
    )
    return list_of_subs


def is_table(name):
    """Check if table exists"""

    with psycopg2.connect(db) as conn:
        with conn.cursor() as cur:
            try:  # TODO doesn't work
                cur.execute(f"SELECT * FROM information_schema.tables WHERE table_schema = 'public';")
                tables = cur.fetchone()

                if name in tables:
                    return True
                return False

            except psycopg2.DatabaseError:
                return False

# from guide

# create tables

# import psycopg2
# from config import config
#
#
# def create_tables():
#     """ create tables in the PostgreSQL database"""
#     commands = (
#         """
#         CREATE TABLE vendors (
#             vendor_id SERIAL PRIMARY KEY,
#             vendor_name VARCHAR(255) NOT NULL
#         )
#         """,
#         """ CREATE TABLE parts (
#                 part_id SERIAL PRIMARY KEY,
#                 part_name VARCHAR(255) NOT NULL
#                 )
#         """,
#         """
#         CREATE TABLE part_drawings (
#                 part_id INTEGER PRIMARY KEY,
#                 file_extension VARCHAR(5) NOT NULL,
#                 drawing_data BYTEA NOT NULL,
#                 FOREIGN KEY (part_id)
#                 REFERENCES parts (part_id)
#                 ON UPDATE CASCADE ON DELETE CASCADE
#         )
#         """,
#         """
#         CREATE TABLE vendor_parts (
#                 vendor_id INTEGER NOT NULL,
#                 part_id INTEGER NOT NULL,
#                 PRIMARY KEY (vendor_id , part_id),
#                 FOREIGN KEY (vendor_id)
#                     REFERENCES vendors (vendor_id)
#                     ON UPDATE CASCADE ON DELETE CASCADE,
#                 FOREIGN KEY (part_id)
#                     REFERENCES parts (part_id)
#                     ON UPDATE CASCADE ON DELETE CASCADE
#         )
#         """)
#     conn = None
#     try:
#         # read the connection parameters
#         params = config()
#         # connect to the PostgreSQL server
#         conn = psycopg2.connect(**params)
#         cur = conn.cursor()
#         # create table one by one
#         for command in commands:
#             cur.execute(command)
#         # close communication with the PostgreSQL database server
#         cur.close()
#         # commit the changes
#         conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#
#
# if __name__ == '__main__':
#     create_tables()

# insert data

# import psycopg2
# from config import config
#
#
# def insert_vendor(vendor_name):
#     """ insert a new vendor into the vendors table """
#     sql = """INSERT INTO vendors(vendor_name)
#              VALUES(%s) RETURNING vendor_id;"""
#     conn = None
#     vendor_id = None
#     try:
#         # read database configuration
#         params = config()
#         # connect to the PostgreSQL database
#         conn = psycopg2.connect(**params)
#         # create a new cursor
#         cur = conn.cursor()
#         # execute the INSERT statement
#         cur.execute(sql, (vendor_name,))
#         # get the generated id back
#         vendor_id = cur.fetchone()[0]
#         # commit the changes to the database
#         conn.commit()
#         # close communication with the database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#
#     return vendor_id

# update data

# !/usr/bin/python
#
# import psycopg2
# from config import config
#
#
# def update_vendor(vendor_id, vendor_name):
#     """ update vendor name based on the vendor id """
#     sql = """ UPDATE vendors
#                 SET vendor_name = %s
#                 WHERE vendor_id = %s"""
#     conn = None
#     updated_rows = 0
#     try:
#         # read database configuration
#         params = config()
#         # connect to the PostgreSQL database
#         conn = psycopg2.connect(**params)
#         # create a new cursor
#         cur = conn.cursor()
#         # execute the UPDATE  statement
#         cur.execute(sql, (vendor_name, vendor_id))
#         # get the number of updated rows
#         updated_rows = cur.rowcount
#         # Commit the changes to the database
#         conn.commit()
#         # Close communication with the PostgreSQL database
#         cur.close()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()
#
#     return updated_rows
#
#
# if __name__ == '__main__':
#     # Update vendor id 1
#     update_vendor(1, "3M Corp")

# link: https://www.postgresqltutorial.com/postgresql-python/
