from page_rank import Rank, Node
import json


def load_data(path=None):
    if not path: path = './mir/content.json'
    with open(path) as file:
        data = json.load(file)
    
    return [Node(article['id'], article['references'], authors=article['authors']) for article in data]


def authors_rank():    
    papers = load_data()
    graph = Rank(papers)

    g = {} 
    authors = set()

    for paper in papers:
        try:
            authors.update(paper.authors)
        except:
            continue
        

    for author in authors:
        try:
            g[author] = set()
        except:
            continue
    
    for paper in papers:
        if not paper.authors: continue
        for author in paper.authors:
            for des in paper.references:
                des = graph.get_node(des)
                if des:
                    for referenced_author in des.node.authors:
                        g[author].add(referenced_author)
    
    return [Node(author, g[author]) for author in g.keys()]
