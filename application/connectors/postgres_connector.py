from sqlalchemy import create_engine, text
from application.connectors.base_connector import BaseConnector
from application.connectors.connector_factory import register_connector
from application.utils.exceptions import AppException


@register_connector("postgresql")
class PostgresConnector(BaseConnector):
    def __init__(self, connection_name, host, port, username, password, database, **config):
        super().__init__(**config)
        self.connection_name = connection_name
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database or "postgres"
        url = f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{self.database}"
        self.engine = create_engine(url)

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            raise AppException(f"PostgreSQL connection failed: {str(e)}", 400)

    def list_databases(self):
        query = "SELECT datname FROM pg_database WHERE datistemplate = false"

        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            return [row[0] for row in result]

    def list_tables(self):
        query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public'
        """

        with self.engine.connect() as conn:
            result = conn.execute(text(query))
            return [row[0] for row in result]

    def list_columns(self, table):
        query = """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = :table
        """

        with self.engine.connect() as conn:
            result = conn.execute(text(query), {"table": table})
            return [row[0] for row in result]

    def fetch_preview(self, table: str, columns: list, limit: int = 10):
        try:
            valid_tables = self.list_tables()
            if table not in valid_tables:
                raise AppException("Invalid table name", 400)

            valid_columns = self.list_columns(table)
            for col in columns:
                if col not in valid_columns:
                    raise AppException(f"Invalid column: {col}", 400)

            cols = ", ".join(columns)

            query = text(f"""
                SELECT {cols}
                FROM {table}
                LIMIT :limit
            """)

            with self.engine.connect() as conn:
                result = conn.execute(query, {"limit": limit})

                rows = result.fetchall()
                column_names = result.keys()

                return [dict(zip(column_names, row)) for row in rows]

        except Exception as e:
            raise AppException(f"Preview fetch failed: {str(e)}", 400)