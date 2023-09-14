import psycopg2


class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="dbname",
            user="user",
            password="password",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()

        # Create tables if they don't exist
        create_contract_table_query = """
        CREATE TABLE IF NOT EXISTS contracts (
            id serial PRIMARY KEY,
            contract_name VARCHAR NOT NULL,
            creation_date TIMESTAMP NOT NULL,
            signing_date TIMESTAMP,
            status VARCHAR NOT NULL,
            project_id INT
        );
        """
        create_project_table_query = """
        CREATE TABLE IF NOT EXISTS projects (
            id serial PRIMARY KEY,
            project_name VARCHAR NOT NULL,
            creation_date TIMESTAMP NOT NULL
        );
        """
        self.execute(create_contract_table_query)
        self.execute(create_project_table_query)
        self.commit()

    def close(self):
        self.cur.close()
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def execute(self, query, values=None):
        self.cur.execute(query, values)
