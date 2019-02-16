"""
migrator.py

Used to migrate the database from previous versions to the current version used by diddlebot.

:author Sam Kuzio
"""

# The current version of the database that this version of diddlebot needs to run.
# This value is used to determine when and how to migrate the database.
DB_MAX_VERSION = 1


def migrate(conn):
    """
    Performs high level migration tasks.
    :param conn: The database connection to use while migrating.
    :return: None
    """

    db_version = get_db_version(conn)

    if db_version == DB_MAX_VERSION:
        print("Database is up to date - no changes need to be applied.")
        return

    print("Migrating database from version " + str(db_version) + " to version " + str(DB_MAX_VERSION))

    # Dictionary that maps a database version to the next update it should apply.
    migrations = {
        0: 'v1_migration.sql',
    }

    # Apply all of the database versions.
    while db_version < DB_MAX_VERSION:
        apply_migration(conn, db_version, migrations[db_version])

        # This is technically not the most efficient thing as we could just add one to the
        # db version, but this will cause issues should one of our migrations forget to update
        # the stored version number
        db_version = get_db_version(conn)

    print("Database has been successfully updated to " + str(DB_MAX_VERSION))


def get_db_version(conn):
    """
    Returns the version of the database. If the version of the database is not stored
    in the database, this will create the version table and initialize the version to 0.
    :param conn: the database connection
    :return: The version of the database.
    """

    c = conn.cursor()

    # Create the version table if it doesn't exist.
    sql = "CREATE TABLE IF NOT EXISTS database_version (number INTEGER PRIMARY KEY)"
    c.execute(sql)
    conn.commit()

    # get the db version (there should only ever be one row in this table)
    sql = "SELECT * FROM database_version"
    c.execute(sql)
    version = c.fetchone()

    if version is not None:
        return version[0]

    # If there is no version in the table, we must set the version to 0.
    set_db_version(0, conn)
    return 0


def set_db_version(version, conn):
    """
    Set the version of the database contained in the database_version table to the given number.
    :param version: The version of the database.
    :param conn: The connection to the database.
    :return: None
    """

    c = conn.cursor()

    # Drop all rows from the table (effectively removing the current version)
    sql = "DELETE FROM database_version"
    c.execute(sql)

    # Now insert the value
    t = (version,)
    sql = "INSERT INTO database_version VALUES (?)"
    c.execute(sql, t)

    # must commit changes to ensure they save.
    conn.commit()


def read_migration_file(fname):
    """
    Reads the contents of a migration file. Assumes that a file exists with the given
    name in the db directory (next to this python file).
    :param fname: The name of the migration file, including any file extension.
    :return: The contents of the migration file.
    """
    with open('./src/db/' + fname) as file:
        text = file.read()
    return text


def apply_migration(conn, version, file):
    """
    Updates the database to the given version using the provided file.
    :param conn: The database connection
    :param version: The current version of the database.
    :param file: The name of the migration file to load. Assumes that this file
                 exists along side this script file.
    :return: None
    """

    print("Migrating to v" + str(version + 1))
    c = conn.cursor()

    # Create the quips table
    sql = read_migration_file(file)
    for statement in sql.split(";"):
        c.execute(statement)

    conn.commit()

    set_db_version(version + 1, conn)
