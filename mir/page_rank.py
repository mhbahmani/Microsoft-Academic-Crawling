from classes import Data, Node
import json
import utils
import sys


args = sys.argv[1:]

ALPHA = float(args[1])
PR_VALUE = float(args[3])


class Rank:
    def __init__(self, Nodes, alpha):
        self.nodes: list = Nodes
        self.data: dict = {}
        for node in Nodes:
            self.data[node.id] = Data(
                node, PR_VALUE, PR_VALUE, 1, 1, 1, 1)
        self.alpha = alpha

    def iter_hits(self, n):
        for _ in range(n):
            for data in self.data.values():
                des_nodes = data.Node.references
                for des_node in des_nodes:
                    if des_node in self.data.keys():
                        data.hub_tmp += self.data[des_node].auth 
                        self.data[des_node].auth_tmp += data.hub

            self.set_data()

    def get_Node(self, id=None):
        return self.data[id]

    def set_data(self):
        for key in self.data.keys():
            self.data[key].page_rank = self.data[key].tmp
            self.data[key].auth = self.data[key].auth_tmp
            self.data[key].hub = self.data[key].hub_tmp

        for key in self.data.keys():
            self.data[key].auth_tmp = 0
            self.data[key].hub_tmp = 0

    def iterate(self, n):
        for _ in range(n):
            for data in self.data.values():
                if len(data.node.references) > 0:
                    conferred_value = (
                        data.page_rank / len(data.node.references)) * self.alpha
                    des_nodes = data.node.references
                    for des_Node in des_nodes:
                        if des_Node in self.data.keys():
                            self.data[des_Node].tmp += conferred_value

            self.set_data()

    def get_page_ranks(self):
        page_ranks = {}
        for d in self.data.values():
            page_ranks[d.node.id] = d.page_rank
        return page_ranks

    def get_hit_rank(self):
        top_ids = sorted(
            self.data,
            key=lambda id: self.data[id].auth,
            reverse=True)[:10]
        top_auth = {}
        for id in top_ids:
            top_auth[id] = self.get_Node(id).auth

        return top_auth


if __name__ == '__main__':

    nodes = utils.load_data()
    graph = Rank(nodes, ALPHA)
    graph.iterate(5)
    page_ranks = json.dumps(graph.get_page_ranks(), indent=3)
    # utils.create_authors_Rank()
