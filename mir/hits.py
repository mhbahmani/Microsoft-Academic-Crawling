from main import Graph, ALPHA, NUMBER_OF_ITERATIONS
from utils import load_hits_data, make_hits_results
from pprint import pprint


def hits():
    graph = Graph(load_hits_data(), ALPHA)
    graph.calc_score_with_hits(NUMBER_OF_ITERATIONS)
    pprint(make_hits_results(graph))


if __name__ == '__main__':
    hits()