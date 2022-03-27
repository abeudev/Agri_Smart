import sqlite3


def create_connection(db_name):

    connection = None

    try:
        connection = sqlite3.connect(db_name)
    except sqlite3.Error as e:
        print(e)

    return connection

def create_fields_table(connection):

    sql_cmd = """
        CREATE TABLE IF NOT EXISTS field(
            id   integer PRIMARY KEY,
            name text NOT NULL,
            geometry text NOT NULL,
            crop text NOT NULL,
            area float NOT NULL
        ); """

    try:
        cursor = connection.cursor()
        cursor.execute(sql_cmd)
    except sqlite3.Error as e:
        print(e)


def install():

    connection = create_connection('openagriculture/openagriculture.db')

    if connection is not None:

        create_fields_table(connection)
    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    install()