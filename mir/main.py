from classes import Data, Node
import sys

args = sys.argv[1:]
PATH = args[1]
ALPHA = float(args[3])
PR_VALUE = float(args[5])
NUMBER_OF_ITERATIONS = int(args[7])



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

    def calc_score_with_hits(self, n):
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

    def calc_score_with_page_rank(self, n):
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