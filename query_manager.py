from postgres_query import PostgresQueryExecutor


class QueryManager:

    def __init__(self):
        self.postgres_instance = PostgresQueryExecutor('discord_db')

    def create_user_history(self, user_id, username, search_term):
        query = "INSERT INTO user_history(user_id, username, search_term) values('{user_id}', '{username}', '{search_term}')".\
            format(user_id=user_id, username=username, search_term=search_term)

        self.postgres_instance.execute_query(query)

    def search_history(self, user_id, search_term):
        query = "SELECT * FROM user_history where user_id='{user_id}' and search_term='{search_term}'".\
            format(user_id=user_id, search_term=search_term)

        return self.postgres_instance.execute(query)

    def update_user_history(self, user_id, search_term, updated_at):
        query = "UPDATE user_history set updated_at='{updated_at}' where user_id='{user_id}' and search_term='{search_term}'".\
            format(user_id=user_id, search_term=search_term, updated_at=updated_at)

        self.postgres_instance.execute_query(query)

    def search_recent_history(self, user_id, search_term):
        query = "SELECT * FROM user_history where user_id='{user_id}' and search_term LIKE '%{search_term}%' order by updated_at desc".\
            format(user_id=user_id, search_term=search_term)

        return self.postgres_instance.execute(query)
