import psycopg2


def get_con() -> str:
    conn: object = psycopg2.connect("dbname=log user=postgres host=localhost password=1")

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute("CREATE TABLE if not exists my_test(id serial PRIMARY KEY, num integer, data varchar);")

    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    cur.execute("INSERT INTO log (id, phrase) VALUES (%s, %s)", (100, "abc'def"))

    # Query the database and obtain data as Python objects
    cur.execute("SELECT * FROM my_test;")
    cur.fetchone()
    (1, 100, "abc'def")

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()
    return 'well done'


print(get_con())