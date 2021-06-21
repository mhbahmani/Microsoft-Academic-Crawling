from dataclasses import dataclass


@dataclass
class Node:
    id: int 
    references: list
    abstract: str = None


@dataclass
class Data:
    node: Node
    page_rank: float
    hub: float
    auth: float
    tmp: float
    auth_tmp: float
    hub_tmp: float
