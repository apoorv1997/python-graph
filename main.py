from pypdf import PdfReader
from collections import Counter
from extract import extract_text, remove_header, remove_speaker
from preproc import remove_stopwords, split_sentences, tokenize
import networkx as nx
import json

def main():
    text = extract_text("text.pdf")
    text = remove_header(text)
    text = remove_speaker(text)
    listStr = split_sentences(text)
    # print(listStr)
    mainTokenList = []
    for sentence in listStr:
        tokens = tokenize(sentence)
        tokens = remove_stopwords(tokens)
        # print(tokens)
        if tokens != []:
            mainTokenList.append(tokens)

    # print(mainTokenList)
    counterList = []
    for tokenList in mainTokenList:
        counter = Counter(tokenList)
        counterList.append(counter)

    # for i in range(len(counterList)):
    #     print(f"Counter {i}: {list(counterList[i].keys())}")
    
    edgeWeightDict = {}

    for i in range(len(counterList)):
        edgeWeightDict[i] = []
        for j in range(len(counterList)):
            if i != j:
                commonwords = set(counterList[i].keys()) & set(counterList[j].keys())
                if commonwords:
                    edgeWeightDict[i].append((j, len(commonwords)))

    for key, value in edgeWeightDict.items():
        print(f"counter {list(counterList[key].keys())}")
        for idx, words in value:
            print(f" common words with counter {list(counterList[idx].keys())}: {words}")

    G_original = build_directed_nx_graph(edgeWeightDict)
    scc_list = list(nx.strongly_connected_components(G_original))

    for i, comp in enumerate(scc_list, start=1):
        print(f"SCC {i} (size={len(comp)}): {comp}")

        # 5. Build the SCC DAG in non-decreasing order of SCC size
    scc_dag = build_scc_dag(G_original, scc_list)

    # 6. Export the SCC DAG (not the original graph) to data.txt
    export_graph_to_file(scc_dag, filename="data.txt")
    print("\nSCC DAG has been exported to 'data.txt'.")


def build_directed_nx_graph(edgeWeightDict):
    """
    Create a NetworkX DiGraph from the edgeWeightDict:
      edgeWeightDict[node] = list of (other_node, weight).
    """
    G = nx.DiGraph()
    G.add_nodes_from(edgeWeightDict.keys())
    for source, edges in edgeWeightDict.items():
        for (target, w) in edges:
            G.add_edge(source, target, weight=w)
    return G

def build_scc_dag(G_original, scc_list):
    """
    Build a Directed Acyclic Graph (DAG) of SCCs:
      1) Sort SCCs in non-decreasing order of their size (len of each set).
      2) Create one super-node per SCC (SCC_0, SCC_1, ...).
      3) Add edges between these super-nodes if an edge exists between any
         two SCCs in the original graph.
    """
    # 1. Sort the SCCs by their size (ascending)
    sorted_sccs = sorted(enumerate(scc_list), key=lambda x: len(x[1]))
    # sorted_sccs = [(old_scc_index, {node1, node2, ...}), ...]

    # Create a new directed graph (the DAG of SCCs)
    new_dag = nx.DiGraph()

    # 2. Add a node in the DAG for each SCC
    # We'll label them "SCC_0", "SCC_1", ... in ascending size order
    for rank, (old_idx, nodes_set) in enumerate(sorted_sccs):
        dag_node_id = f"SCC_{rank}"
        new_dag.add_node(
            dag_node_id,
            size=len(nodes_set),       # how many original nodes in this SCC
            original_index=old_idx,    # where it appeared in the unsorted scc_list
            members=list(nodes_set)    # which original nodes are in this SCC
        )

    # 3. Map each original node -> which DAG SCC node it belongs to
    node_to_scc = {}
    for rank, (old_idx, nodes_set) in enumerate(sorted_sccs):
        dag_node_id = f"SCC_{rank}"
        for n in nodes_set:
            node_to_scc[n] = dag_node_id

    # 4. For every edge (u -> v) in the original graph, if u and v
    #    belong to different SCCs, add an edge in the DAG
    for (u, v) in G_original.edges():
        scc_u = node_to_scc[u]
        scc_v = node_to_scc[v]
        if scc_u != scc_v:
            new_dag.add_edge(scc_u, scc_v)

    return new_dag

def export_graph_to_file(G, filename="data.txt"):
    """
    Exports a NetworkX DiGraph (the SCC DAG) into a JSON structure:
      { "nodes": [...], "links": [...] }
    Each DAG node has id, size, members. Each link has source, target.
    """
    # Node data
    nodes_data = []
    for node_id, attrs in G.nodes(data=True):
        node_info = {
            "id": node_id,
            "size": attrs.get("size", 1),
            "members": attrs.get("members", [])
        }
        nodes_data.append(node_info)

    # Edge data
    links_data = []
    for (u, v) in G.edges():
        links_data.append({
            "source": u,
            "target": v
        })

    # Combined graph structure
    graph_data = {
        "nodes": nodes_data,
        "links": links_data
    }

    # Write to file
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2)
    print(f"DAG data has been written to '{filename}'.")

if __name__ == "__main__":
    # calling the main function
    main()