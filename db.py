import sqlite3
import logging


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file, check_same_thread=False)
        logging.info(f"Connected to SQLite. SQLite version: {sqlite3.version}")
    except sqlite3.Error as e:
        logging.error(e)
    return conn


def create_table(conn):
    """ create a table with timestamp as primary key """
    try:
        sql_create_table = """
        CREATE TABLE IF NOT EXISTS conversations (
            timestamp TEXT NOT NULL PRIMARY KEY,
            conversation_id TEXT NOT NULL
        );
        """
        cursor = conn.cursor()
        cursor.execute(sql_create_table)
        print("Table created successfully")
    except sqlite3.Error as e:
        print(e)


def start_db_connection():
    # start DB connection
    db_path = './data/convo.db'
    conn = create_connection(db_path)
    if conn is not None:
        create_table(conn)
        return conn
    else:
        raise Exception("Error! Cannot create the database connection.")


def get_conversation_id(conn, timestamp):
    """
    Query conversation_id by timestamp
    :param conn: Connection object
    :param timestamp: string, the primary key to query for
    :return: conversation_id if found, otherwise None
    """
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT conversation_id FROM conversations WHERE timestamp=?", (timestamp,))
        row = cursor.fetchone()
        if row:
            return row[0]  # Return the conversation_id found
        else:
            return None  # No data found for the given timestamp
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None


def insert_entry(conn, timestamp, conversation_id):
    """
    Insert a new entry into the conversations table
    :param conn: Connection object
    :param timestamp: string
    :param conversation_id: string
    :return:
    """
    cursor = conn.cursor()
    # Check if the timestamp already exists
    cursor.execute("SELECT * FROM conversations WHERE timestamp=?", (timestamp,))
    data = cursor.fetchone()
    if data is not None:
        print("Entry already exists for the given timestamp.")
        return False

    try:
        sql_insert = """INSERT INTO conversations (timestamp, conversation_id) VALUES (?, ?);"""
        cursor.execute(sql_insert, (timestamp, conversation_id))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(e)
        return False
