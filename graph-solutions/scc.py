from collections import defaultdict
import networkx as nx

def find_scc(graph):
    """Finds SCCs using Tarjan's Algorithm."""
    index = 0
    stack = []
    in_stack = set()
    indices = {}
    low_link = {}
    sccs = []

    def strongconnect(node):
        """function that will do the DFS traversal using stack"""
        nonlocal index
        indices[node] = low_link[node] = index
        index += 1
        stack.append(node)
        in_stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in indices:
                strongconnect(neighbor)
                low_link[node] = min(low_link[node], low_link[neighbor])
            elif neighbor in in_stack:
                low_link[node] = min(low_link[node], indices[neighbor])

        # here we find that we are now at root node again, so we pop all the nodes
        if low_link[node] == indices[node]:
            scc = []
            while stack:
                v = stack.pop()
                in_stack.remove(v)
                scc.append(v)
                if v == node:
                    break
            sccs.append(scc)

    # Run DFS on all nodes
    for node in list(graph):
        if node not in indices:
            strongconnect(node)

    return sccs


def find_dag(graph, scc_list):
    """function to create DAG for SCC list."""
    dag = nx.DiGraph()
    node_to_scc = {}
    for i, scc in enumerate(scc_list):
        for node in scc:
            node_to_scc[node] = i
    
    for u in graph:
        for v in graph[u]:
            scc_u = node_to_scc[u]
            scc_v = node_to_scc[v]
            if scc_u != scc_v:
                dag.add_edge(scc_u, scc_v)
    
    return dag