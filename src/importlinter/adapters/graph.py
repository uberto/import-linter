"""
Graph adapter that can switch between different search algorithms.
"""
import copy
from typing import Set, Tuple

from grimp import ImportGraph

from importlinter.application.graph_utils import find_shortest_chains_breadth_first


class ImportGraphWithBFS:
    """
    Wrapper around ImportGraph that can use BFS algorithm for finding shortest chains.
    """
    
    def __init__(self, graph: ImportGraph, use_bfs: bool = True):
        self._graph = graph
        self._use_bfs = use_bfs
    
    def find_shortest_chains(
        self, 
        importer: str, 
        imported: str, 
        as_packages: bool = True
    ) -> Set[Tuple[str, ...]]:
        """
        Find shortest chains using either BFS or the original algorithm.
        """

        if self._use_bfs:
            return find_shortest_chains_breadth_first(
                graph=self._graph,
                importer=importer,
                imported=imported,
                as_packages=as_packages
            )
        else:
            return self._graph.find_shortest_chains(
                importer=importer,
                imported=imported,
                as_packages=as_packages
            )
    
    def __deepcopy__(self, memo):
        """
        Custom deepcopy to preserve the BFS wrapper.
        """
        copied_graph = copy.deepcopy(self._graph, memo)
        return ImportGraphWithBFS(copied_graph, self._use_bfs)
    
    def __getattr__(self, name):
        """
        Delegate all other methods to the wrapped graph.
        """
        return getattr(self._graph, name)
