import json
import psycopg2
import psycopg2.extras

from datetime import datetime

from settings import DISCORD_DB_HOST, DISCORD_DB_NAME, DISCORD_DB_PASSWORD, DISCORD_DB_USER


class PostgresRestultJSONSerializer:
    """Converts the results to JSON"""

    @staticmethod
    def alchemyencoder(obj):
        """JSON encoder function for SQLAlchemy special classes."""
        if isinstance(obj, datetime):
            return obj.isoformat()

    @staticmethod
    def parse(results):
        return json.loads(json.dumps([dict(result) for result in results],
                                     default=PostgresRestultJSONSerializer.alchemyencoder))


class PostgresQueryExecutor(object):
    """
    Directly interacts with the database.
    """
    DB = {
        'discord_db': {
            "user": DISCORD_DB_USER,
            "password": DISCORD_DB_PASSWORD,
            "host": DISCORD_DB_HOST,
            "port": 5432,
            "database": DISCORD_DB_NAME
        }
    }

    def __init__(self, db):
        """
            init the connection and the postgres cursor.
        """
        self.connection = psycopg2.connect(**PostgresQueryExecutor.DB[db])
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def close(self):
        """
        Close the connection and postgres cursor
        """
        self.cursor.close()
        self.connection.close()

    def execute(self, query, **kwargs):
        """
        Fetch the result from DB
        """
        print('Executing Query: {}'.format(query.format(**kwargs)))

        self.cursor.execute(query.format(**kwargs))
        data = PostgresRestultJSONSerializer.parse(self.cursor.fetchall())
        return data

    def execute_query(self, query, **kwargs):
        """
        Execute create/update/delete query
        """
        print('Executing Query: {}'.format(query.format(**kwargs)))

        self.cursor.execute(query.format(**kwargs))
        self.commit()

    def commit(self):
        """
        Commit the DB
        """
        self.connection.commit()
