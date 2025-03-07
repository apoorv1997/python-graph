from pypdf import PdfReader
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
from collections import Counter, defaultdict
from scc import find_dag, find_scc
from utility import utility



def create_undirected_list(edgeWeightDict):
    undirected_graph = defaultdict(set)
    for node, neighbors in edgeWeightDict.items():
        for neighbor in neighbors:
            undirected_graph[node].add(neighbor) 
            undirected_graph[neighbor].add(node)
    return undirected_graph

def plot_undirected_distribution(graph):
    G = nx.Graph(graph)

    degrees = [degree for node, degree in G.degree()]

    # Plot the degree distribution
    plt.figure(figsize=(10, 10))
    plt.hist(degrees, bins=range(min(degrees), max(degrees) + 1), alpha=0.75, edgecolor='black')
    plt.title('Un-directed Degree Distribution of the Graph')
    plt.xlabel('Degree')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig('degree-dist.png')
    plt.show(block=False)


def create_adjacency_list(counterList, wordToCounterList):

    edgeWeightDict = defaultdict(dict)

    for i, counter in wordToCounterList.items(): 
        node = list(counter)
        for i in range(len(node)):
            for j in range(i+1, len(node)):
                u, v = node[i], node[j]
                commonWords = set(counterList[i]) & set(counterList[j])
                weight = len(commonWords)
                if weight > 0:
                    edgeWeightDict[u][v] = weight
    return edgeWeightDict

def plot_indegree_outdegree_distribution(edgeWeightDict):
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)

    for node, neighbours in edgeWeightDict.items():
        out_degree[node] = sum(neighbours.values())
        for neighbour, weight in neighbours.items():
            in_degree[neighbour] += weight

    nodes_with_no_degree = set(in_degree.keys()).union(set(out_degree.keys()))

    for node in nodes_with_no_degree:
        in_degree.setdefault(node, 0)
        out_degree.setdefault(node, 0)

    plt.subplot(1, 2, 1)
    plt.hist(in_degree.values(), bins=30, color='blue', alpha=0.4)
    plt.xlabel("Weighted In-Degree")
    plt.ylabel("Frequency")
    plt.title("Weighted In-Degree Distribution")

    # Weighted Out-Degree Distribution
    plt.subplot(1, 2, 2)
    plt.hist(out_degree.values(), bins=30, color='red', alpha=0.4)
    plt.xlabel("Weighted Out-Degree")
    plt.ylabel("Frequency")
    plt.title("Weighted Out-Degree Distribution")

    plt.tight_layout()
    plt.savefig('in_and_out_degree_dist.png')
    plt.show(block=False)


def plot_bcc_forest(graph, bcc_list):
    G = nx.Graph(graph)
    plt.figure(figsize=(12, 12))
    bcc_colors = plt.cm.rainbow(range(len(bcc_list))) 

    for i, bcc in enumerate(bcc_list):
        subgraph = G.subgraph(bcc)
        nx.draw(subgraph, with_labels=True, node_size=500, node_color=[bcc_colors[i]], font_size=10, font_weight='bold', edge_color=[bcc_colors[i]], alpha=0.7)
    
    plt.title("BCCs")
    plt.savefig('bcc_forest.png')
    plt.show(block=False)


def find_bcc(graph):
    """do DFS and compute low and pre time"""
    index = 0
    stack = []
    pre = {} 
    low = {}
    parent = {}
    bccs = []

    def dfs(u):
        """function will do DFS and compute pre and low time and store parents for each visited nodes"""
        nonlocal index
        pre[u] = low[u] = index
        index += 1
        stack.append(u)
        
        for v in graph[u]:
            if v not in pre:
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                
                # checking if u is seperation vertex, then we will pop all nodes from stack and it forms a BCC
                if low[v] >= pre[u]:
                    bcc = []
                    while stack[-1] != v:
                        bcc.append(stack.pop())
                    bcc.append(stack.pop())
                    bcc.append(u)
                    bccs.append(bcc)
            elif v != parent.get(u):  # this shows that there is a back edge
                low[u] = min(low[u], pre[v])

    # running dfs for nodes that are not visited
    for node in graph:
        if node not in pre:
            dfs(node)
    
    return bccs


def find_connected_components(undirected_graph):
    visited = set()
    connected_components = 0
    
    for node in undirected_graph:
        if node not in visited:
            dfs(node, undirected_graph, visited)
            connected_components += 1
    
    return connected_components

def dfs(node, graph, visited):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(neighbor, graph, visited)

def plot_scc_degree_distribution(scc_dict, edgeWeightDict):
    scc_sizes = [len(scc) for scc in scc_dict]
    scc_edge_counts = []
    for scc in scc_dict:
        edge_count = 0
        for node in scc:
            for neighbor in edgeWeightDict.get(node, {}):
                if neighbor in scc: 
                    edge_count += 1
        scc_edge_counts.append(edge_count)

    plt.figure(figsize=(12, 5))
    plt.subplot(1, 2, 1)
    plt.hist(scc_sizes, bins=30, color='blue', alpha=0.7)
    plt.xlabel("Number of Vertices in SCC")
    plt.ylabel("Frequency of vertices")
    plt.title("SCC Size Distribution")

    plt.subplot(1, 2, 2)
    plt.hist(scc_edge_counts, bins=30, color='red', alpha=0.7)
    plt.xlabel("Number of Edges in SCC")
    plt.ylabel("Frequency of edges")
    plt.title("SCC Edge Distribution")

    plt.tight_layout()
    plt.savefig('scc_size.png')
    plt.show()


def main():
    counterList = utility()

    
    wordToCounterList = defaultdict(set) # hashset to add counter for O(1) retrieval

    for i, counter in enumerate(counterList):
        for word in counter:
            wordToCounterList[word].add(i)
      
    edgeWeightDict = create_adjacency_list(counterList, wordToCounterList)
    # for node, edge in edgeWeightDict.items():
    #     print(f"Counter {counterList[node].keys()} -> {len(edge)}")
    # for key, value in edgeWeightDict.items():
    #     print(f"counter {list(counterList[key].keys())}")
    #     for idx, words in value.items():
    #         print(f" common words with counter {list(counterList[idx].keys())}: {words}")

    vertices = len(edgeWeightDict)
    edges = sum([len(neighbours) for neighbours in edgeWeightDict.values()])
    print(f"Number of vertices: {vertices}")
    print(f"Number of edges: {edges}")
    scc_list = find_scc(edgeWeightDict)
    plot_indegree_outdegree_distribution(edgeWeightDict)
    plot_scc_degree_distribution(scc_list, edgeWeightDict)
    undirected_graph_list = create_undirected_list(edgeWeightDict)
    plot_undirected_distribution(undirected_graph_list)
    total_connected_components = find_connected_components(undirected_graph_list)
    # print(f"Total Connected Components: {total_connected_components}")
    bcc_list = find_bcc(undirected_graph_list)
    # print(f"Total number of Biconnected Components: {len(bcc_list)}")
    plot_bcc_forest(undirected_graph_list, bcc_list)
    dag_list = find_dag(edgeWeightDict, scc_list)

    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(dag_list, k=0.5, iterations=50)
    nx.draw(dag_list, pos, with_labels=True, node_size=1000, node_color='skyblue', font_size=12, font_weight='bold', edge_color='gray')
    plt.title("DAG of SCCs")
    plt.show()

    with open("size.txt", "w") as f:
        f.write(f"Number of vertices: {vertices}\n")
        f.write(f"Number of edges: {edges}\n")
        f.write(f"Total Strongly Connected Components: {len(scc_list)}\n")
        f.write(f"Total Connected Components: {total_connected_components}\n")
        f.write(f"Total number of Biconnected Components: {len(bcc_list)}\n")
    # G = nx.Graph()

    # Add edges to the graph
    # for node, edges in counterWordAdjacencyList.items():
    #     for neighbor, weight in edges:
    #         G.add_edge(node, neighbor, weight=weight)


    plt.figure(figsize=(30, 30))
    pos = nx.fruchterman_reingold_layout(G)  # Alternative: nx.fruchterman_reingold_layout(G)
    edge_labels = {(u, v): d["weight"] for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=100, font_size=12, font_weight="bold")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    plt.title("Optimized Graph Visualization (500 Nodes)")
    plt.show()
    net = Network(notebook=True, width="1000px", height="800px", bgcolor="#222222", font_color="white")
    for node in G.nodes():
        net.add_node(node, label=str(node), color="blue") 

    for u, v, d in G.edges(data=True):
        net.add_edge(u, v, value=d['weight'])
    #     print(f"Counter {edgeWeightDict[node]} -> {len(edges)}")
    net.show("example.html")
if __name__ == "__main__":
    # calling the main function
    main()