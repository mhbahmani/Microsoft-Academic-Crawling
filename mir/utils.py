from main import Graph, Node
import json


def load_page_rank_data():
    return read_data_from_file()


def load_hits_data():
    return authors_referenced(read_data_from_file())


def read_data_from_file(path=None):
    if not path: path = './mir/content.json'
    with open(path) as file:
        data = json.load(file)
    
    return [Node(article['id'], article['references'], authors=article['authors']) for article in data]


def authors_referenced(data):    
    graph = Graph(data)

    author_referenced_to = {} 
    authors = set()
    authors_updated = set()

    for paper in data:
        try:
            authors_updated.update(paper.authors)
            for author in authors_updated - authors:
                author_referenced_to[author] = set()
            authors.update(paper.authors)
        except:
            continue
    
    # making a list of authors that each author referenced to
    for paper in data:
        if not paper.authors: continue
        for author in paper.authors:
            for ref in paper.references:
                ref = graph.get_node(ref)
                if not ref: continue
                for ref_author in ref.node.authors:
                    author_referenced_to[author].add(ref_author)
    
    return [Node(author, author_referenced_to[author]) for author in author_referenced_to.keys()]


def make_page_ranks_results(graph):
    page_ranks = {}
    for d in graph.data.values():
        page_ranks[d.node.id] = d.page_rank
    return page_ranks

def make_hits_results(graph):
    top_ids = sorted(
        graph.data,
        key=lambda id: graph.data[id].score,
        reverse=True
    )[:20]

    top_authors = {}
    for id in top_ids:
        top_authors[id] = graph.get_node(id).score

    return top_authors