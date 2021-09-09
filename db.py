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
        CREATE TABLE "{name}" (
        id SERIAL PRIMARY KEY,
        channel_name TEXT,
        channel_id TEXT,
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

    command = f"""
    INSERT INTO "{table}" (channel, pattern)
    VALUES {(channel, pattern)} 
    RETURNING id
    ;"""

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


def update(values: dict[str: str], table: str):
    """Change value in db"""

    if not is_table(table):
        return "You don't have any subscriptions yet"

    command = f"""UPDATE "{table}"
                SET {values.keys()[0]} = {values.values()[0]}
                ;"""

    with psycopg2.connect(db) as conn:
        with conn.cursor() as cur:
            cur.execute(command)

    return 'Updated'


def delete(values: dict[str: str], table: str):
    """Delete value from db"""

    if not is_table(table):
        return "You don't have any subscriptions yet"

    command = f"""DELETE FROM "{table}"
                WHERE channel = {values.keys()[0]}
                AND pattern = {values.values()[0]}
                ;"""

    try:
        with psycopg2.connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
    except psycopg2.DatabaseError as error:
        return error

    return 'Deleted'


def get(table: str):
    """Return a string with all user's subs"""

    if not is_table(table):
        return "You don't have any subscriptions yet"

    command = f"""SELECT * FROM "{table}";"""

    with psycopg2.connect(db) as conn:
        with conn.cursor() as cur:
            cur.execute(command)
            list_of_subs = cur.fetchall()

    if not list_of_subs:
        return 'Your list of subs is empty'

    result = ''
    for row in list_of_subs:
        result += f'{row[1]} - {row[2]}\n'

    return result


def is_table(name: str):
    """Check if table exists"""

    with psycopg2.connect(db) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(f"SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'public';")
                tables = cur.fetchone()

                if name in tables:
                    return True
                return False

            except psycopg2.DatabaseError:
                return False

# from guide

# update data

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
