from page_rank import Node
import json


def load_data(path=None):
    if not path: path = 'content.json'
    with open(path) as file:
        data = json.load(file)
    return [Node(article['id'], article['references']) for article in data]
