import psycopg2


class UseDatabase:

    def __init__(self, config: dict) -> None:
        self.configuration = config

    def __enter__(self) -> None:
        self.conn = psycopg2.connect(self.configuration)
        self.cursor = self.conn.cursor

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()