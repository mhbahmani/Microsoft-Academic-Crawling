from classes import Data, Node
from pprint import pprint
import utils
import sys

args = sys.argv[1:]
ALPHA = float(args[1])
PR_VALUE = float(args[3])
NUMBER_OF_ITERATIONS = int(args[5])


class Graph:
    def __init__(self, nodes, alpha=ALPHA):
        self.nodes = nodes
        self.data = {}
        self.alpha = alpha
        self.initialize_data(nodes)

    def initialize_data(self, nodes=[]):
        for node in nodes:
            self.data[node.id] = Data(
                node, PR_VALUE, PR_VALUE, 1, 1, 1, 1)

    def iterate_pages(self, n):
        for _ in range(n):
            for data in self.data.values():
                des_nodes = data.node.references
                for ref in des_nodes:
                    if ref not in self.data.keys(): continue
                    data.hub_tmp += self.data[ref].score
                    self.data[ref].score_tmp += data.hub
            self.update_data()

    def get_node(self, id=None):
        return self.data.get(id)

    def update_data(self):
        for key in self.data.keys():
            self.data[key].page_rank = self.data[key].tmp
            self.data[key].score = self.data[key].score_tmp
            self.data[key].hub = self.data[key].hub_tmp

        for key in self.data.keys():
            self.data[key].score_tmp = 0
            self.data[key].hub_tmp = 0

    def iterate(self, n):
        for _ in range(n):
            for data in self.data.values():
                if not data.node.references: continue
                conferred_value = (
                    data.page_rank / len(data.node.references)) * self.alpha
                des_nodes = data.node.references
                for des_Node in des_nodes:
                    if des_Node not in self.data.keys(): continue
                    self.data[des_Node].tmp += conferred_value
            self.update_data()

    def get_page_ranks(self):
        page_ranks = {}
        for d in self.data.values():
            page_ranks[d.node.id] = d.page_rank
        return page_ranks

    def get_hit_rank(self):
        top_ids = sorted(
            self.data,
            key=lambda id: self.data[id].score,
            reverse=True
        )[:20]

        top_authors = {}
        for id in top_ids:
            top_authors[id] = self.get_node(id).score

        return top_authors


if __name__ == '__main__':
    graph = Graph(utils.load_data())
    graph.iterate(5)
    pprint(graph.get_page_ranks())

    # graph = Graph(utils.authors_rank(), ALPHA)
    # graph.iterate_pages(NUMBER_OF_ITERATIONS)
    # pprint(graph.get_hit_rank())