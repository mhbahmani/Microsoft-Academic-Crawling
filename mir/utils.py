from page_rank import Graph, Node
import json


def load_data(path=None):
    if not path: path = './mir/content.json'
    with open(path) as file:
        data = json.load(file)
    
    return [Node(article['id'], article['references'], authors=article['authors']) for article in data]


def authors_rank():    
    papers = load_data()
    graph = Graph(papers)

    author_referenced_to = {} 
    authors = set()
    authors_updated = set()

    for paper in papers:
        try:
            authors_updated.update(paper.authors)
            for author in authors_updated - authors:
                author_referenced_to[author] = set()
            authors.update(paper.authors)
        except:
            continue
    
    # making a list of authors that each author referenced to
    for paper in papers:
        if not paper.authors: continue
        for author in paper.authors:
            for ref in paper.references:
                ref = graph.get_node(ref)
                if not ref: continue
                for ref_author in ref.node.authors:
                    author_referenced_to[author].add(ref_author)
    
    return [Node(author, author_referenced_to[author]) for author in author_referenced_to.keys()]
