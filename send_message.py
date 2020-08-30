from datetime import datetime

from google_search import google_search
from query_manager import QueryManager


class MessageListener:
    """
    Message Listner API - It will get the message and send the reply string.
    """
    def __init__(self, user):
        self.query_manager_instance = QueryManager()
        # Method map corresponding to the input type. It can be scaled in this way.
        self.method_map = {
            "hi": "say_hi",
            "!google": "search_google",
            "!recent": "get_recent_searches"
        }
        self.user = user

    def send_message(self, message):
        self.command = message.split(" ", 1)

        # Get the corresponding method to process the message
        method = self.method_map.get(self.command[0].lower())
        if method:
            method = getattr(self, method)

            reply_string = method()
            self.query_manager_instance.close()
            return reply_string

    def say_hi(self):
        """
        :return: reply string
        """
        return "hey"

    def search_google(self):
        """
        search on google and create/update the search_keyword in db.
        :return: Top 5 links
        """
        google_query = self.command[1].lower()
        # search on Google API
        results = google_search(google_query)
        if results:
            # Check if the data already exists and then create/update the data.
            self.create_update_db(google_query)
            results = ' \n'.join(results)
            return "The Top five links for your search are  -\n{links}".format(links=results)

        else:
            return "Sorry, there are no matching Links found"

    def get_recent_searches(self):
        """
        Check for recent searches and return in sorted order by last searched.
        :return: recent searches
        """
        google_query = self.command[1].lower()
        result = self.query_manager_instance.search_recent_history(user_id=self.user.id, search_term=google_query)
        if result:
            search_term = [each['search_term'] for each in result]
            search_term = ' \n'.join(search_term)
            return "Your recent search history for this keyword is  -\n{result}".format(result=search_term)
        else:
            return "Sorry, there are not recent search history corresponding to this keyword"

    def create_update_db(self, google_query):
        """
        If user_id-search_term already exists update the updated_at else create an entry in the database
        :param google_query: search keyword
        """
        result = self.query_manager_instance.search_history(user_id=self.user.id, search_term=google_query)
        if result:
            updated_at = datetime.now()
            self.query_manager_instance.update_user_history(user_id=self.user.id, search_term=google_query, updated_at=updated_at)
        else:
            self.query_manager_instance.create_user_history(user_id=self.user.id, username=self.user.name, search_term=google_query)
