from page_rank import Node
import json


def load_data(path=None):
    if not path: path = 'content.json'
    with open(path) as file:
        data = json.load(file)
    return [Node(article['id'], article['references']) for article in data]


def create_authors_Rank(path=None):
    if not path: path = 'content.json'

    papers = Rank(utils.load_data)
    with open(path) as file:
        data = json.load(file)
    authors = set()
    for article in data:
        authors.update(article['authors'])

    g = {}
    for author in authors:
        g[author] = set()
    for paper in papers.data:
        for dest in paper.references:
            node = paper.get_node(dest)
            for authors in node.references:
