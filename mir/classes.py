from dataclasses import dataclass


@dataclass
class Node:
    id: int
    references: list
    abstract: str = None
    authors: list = None


@dataclass
class Data:
    node: Node
    page_rank: float
    score: float
    socore_tmp: float
    tmp: float
    hub: float
    hub_tmp: float
