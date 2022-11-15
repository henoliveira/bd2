import psycopg2


class DbConfig:
    def __init__(
        self,
        connection_data="host=localhost dbname=bd2 user=postgres password=postgres",
    ):
        self.connection_data = connection_data

    def alter(self, query, values):
        try:
            conn = psycopg2.connect(self.connection_data)
        except Exception as e:
            raise e

        try:
            cur = conn.cursor()
            cur.execute(query, values)
            conn.commit()
            return "sucesso"
        except Exception as e:
            conn.rollback()
            print(e)
            return e
        finally:
            cur.close()
            conn.close()
