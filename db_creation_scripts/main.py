import sqlite3

def initdb(dbfile, filename):
    connection = None
    try:
        connection = sqlite3.connect("../databases/" + dbfile)
        print("Database init")

        db_file = open(filename, "r")
        db_cmds = db_file.read().strip().split(";")

        for cmd in db_cmds:
            c = cmd.strip()
            if len(c) > 0:
                connection.execute(cmd.strip())

        connection.commit()
        print("Command runs successful")

    except sqlite3.Error as err:
        print("An error occured:", err)

    finally:
        if connection:
            connection.close()
            print("Sqlite3 connection closed")

initdb("grp9agents.db", "agents.sql")
initdb("grp9customer.db", "customer.sql")
initdb("grp9order.db", "orders.sql")