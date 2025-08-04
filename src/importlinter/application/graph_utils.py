"""
Utilities for working with import graphs.
"""
from typing import Any, Dict, List, Set, Tuple

from grimp import ImportGraph


def find_shortest_chains_breadth_first(
    graph: ImportGraph, 
    importer: str, 
    imported: str, 
    as_packages: bool = True,
    max_depth: int = 0  # Default no check for max depth
) -> Set[Tuple[str, ...]]:
    """
    Find the shortest import chains from importer to imported using breadth-first search.
    
    Args:
        graph: The import graph to search
        importer: The importing module
        imported: The imported module
        as_packages: Whether to treat modules as packages
        max_depth: Maximum depth to search to prevent excessive resource usage
        
    Returns:
        Set of chains (tuples of module names) from importer to imported
    """
    # Queue of paths to explore
    queue = [[(importer)]]
    # Set of chains found
    chains = set()
    # Track the shortest depth we've found a solution at
    shortest_depth = None
    
    while queue:
        path = queue.pop(0)
        node = path[-1]
        current_depth = len(path)

        print("!!! node", node, "depth", current_depth)
        
        # If we've reached the target, add the path to chains
        if node == imported:
            print("!!!target found", node)
            chains.add(tuple(path))
            if shortest_depth is None:
                shortest_depth = current_depth
            continue
            
        # If we've found solutions and this path is longer, skip it
        if shortest_depth is not None and current_depth >= shortest_depth:
            print(f"!!! Skipping {node} at depth {current_depth} because we've already found a solution at depth {shortest_depth}")
            continue
            
        # If we've reached max depth, skip this path
        if 0 < max_depth < current_depth:
            print(f"!!! Skipping {node} at depth {current_depth} because we've reached max depth {max_depth}")
            continue
        
        # Get all modules directly imported by this node
        if as_packages:
            next_modules = graph.find_modules_directly_imported_by(node)
        else:
            # Only consider direct imports between the specific modules
            next_modules = [m for m in graph.find_modules_directly_imported_by(node)
                           if m == imported]
        
        print(f"!!! Found {len(next_modules)} modules imported by {node}: {next_modules}")
        
        for next_module in next_modules:

            print("!!!next_module", next_module)
            # Skip if this would create a cycle in the current path
            if next_module in path:
                print(f"!!! Skipping {next_module} because it would create a cycle")
                continue
                
            # Create a new path with this module
            new_path = list(path)
            new_path.append(next_module)
            queue.append(new_path)
    
    return chains
