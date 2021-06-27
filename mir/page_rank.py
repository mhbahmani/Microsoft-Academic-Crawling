from main import Graph, ALPHA, NUMBER_OF_ITERATIONS, PATH
from utils import load_page_rank_data, make_page_ranks_results
from pprint import pprint


def page_rank():
    graph = Graph(load_page_rank_data(PATH), ALPHA)
    graph.calc_score_with_page_rank(NUMBER_OF_ITERATIONS)
    pprint(make_page_ranks_results(graph))


if __name__ == '__main__':
    page_rank()