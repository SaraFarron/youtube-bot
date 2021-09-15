from psycopg2 import connect, DatabaseError
from main import logger


def execute_sql(command: str):
    """ Execute sql command and returns result"""

    db = 'host=db dbname=postgres user=postgres password=postgres'
    conn = None

    try:
        with connect(db) as conn:
            with conn.cursor() as cur:
                cur.execute(command)
                try:
                    logger.info(f'SQL execute: {command}')
                    response = cur.fetchall()
                except DatabaseError:
                    return ''

    except DatabaseError as error:
        logger.error(error)
        return 'Error'

    if conn is not None:
        conn.close()
    return response


def new_user_table(name: str):
    """Create new user's table"""

    command = f"""
    CREATE TABLE "{name}" (
        id SERIAL PRIMARY KEY,
        channel_name TEXT,
        channel_id TEXT,
        pattern TEXT
        );"""

    response = execute_sql(command)

    if is_table(name):
        return "You are already registered"
    return response


def new_user_subscription(channel_id: str, channel_name: str, pattern: str, user: str):
    """Add new sub"""

    if not is_table(user):
        new_user_table(user)

    command = f"""
        INSERT INTO "{user}" (channel_id, channel_name, pattern)
        VALUES {(channel_id, channel_name, pattern)}
        ;"""

    response = execute_sql(command)

    if response:
        return True
    return False


def add_channel_to_db(channel_id: str, videos: list[str, ]):
    """Add channel to db"""

    command = f"""
            INSERT INTO channels (channel_id, video_0, video_1, video_2, video_3, video_4)
            VALUES {(channel_id, videos[0], videos[1], videos[2], videos[3], videos[4])}
            ;"""

    return execute_sql(command)


def update_row(table: str, old_value: str, new_value: str):
    """Change value in table"""

    command = f"""UPDATE "{table}"
                SET {old_value} = {new_value}
                ;"""

    return execute_sql(command)


def delete_row(table: str, channel_id: str):
    """Delete row from table"""

    command = f"""DELETE FROM "{table}"
                    WHERE channel_id = {channel_id}
                    ;"""

    return execute_sql(command)


def get_value(table: str, field='*'):
    """Get data from table"""

    command = f"""
    SELECT {field} FROM "{table}"
    ;"""

    return execute_sql(command)


def is_table(table: str):
    """Check if table exists"""

    command = f"SELECT * FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
    tables = execute_sql(command)

    if table in tables:
        return True
    return False
