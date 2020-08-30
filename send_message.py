from datetime import datetime

from google_search import google_search
from query_manager import QueryManager


class MessageListener:

    def __init__(self, user):
        self.query_manager_instance = QueryManager()
        self.method_map = {
            "hi": "say_hi",
            "!google": "search_google",
            "!recent": "get_recent_searches"
        }
        self.user = user

    def send_message(self, message):
        self.command = message.split(" ", 1)

        method = self.method_map.get(self.command[0].lower())
        if method:
            method = getattr(self, method)

            return method()

    def say_hi(self):
        return "hey"

    def search_google(self):
        google_query = self.command[1].lower()
        results = google_search(google_query)
        if results:
            self.create_update_db(google_query)
            results = ' \n'.join(results)
            return "The Top five links for your search are  -\n{links}".format(links=results)

        else:
            return "Sorry, there are no matching Links found"

    def get_recent_searches(self):
        google_query = self.command[1].lower()
        result = self.query_manager_instance.search_recent_history(user_id=self.user.id, search_term=google_query)
        if result:
            search_term = [each['search_term'] for each in result]
            search_term = ' \n'.join(search_term)
            return "Your recent search history for this keyword is  -\n{result}".format(result=search_term)
        else:
            return "Sorry, there are not recent search history corresponding to this keyword"

    def create_update_db(self, google_query):
        result = self.query_manager_instance.search_history(user_id=self.user.id, search_term=google_query)
        if result:
            updated_at = datetime.now()
            self.query_manager_instance.update_user_history(user_id=self.user.id, search_term=google_query, updated_at=updated_at)
        else:
            self.query_manager_instance.create_user_history(user_id=self.user.id, username=self.user.name, search_term=google_query)
