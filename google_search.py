from settings import GOOGLE_API_KEY, GOOGLE_CX_KEY
from googleapiclient.discovery import build


def google_search(query):
    service = build("customsearch", "v1",
                    developerKey=GOOGLE_API_KEY)

    result = service.cse().list(
        q=query,
        cx=GOOGLE_CX_KEY,
    ).execute()
    try:
        items = result["items"]
        top_links = []
        for i in items:
            if len(top_links) < 5:
                top_links.append(i["link"])
        print(top_links)
        return top_links

    except Exception as e:
        return
