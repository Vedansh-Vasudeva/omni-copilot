import networkx as nx
import json
import os

class KnowledgeGraph:
    def __init__(self, filepath="./data/kg.json"):
        self.filepath = filepath
        self.graph = nx.DiGraph()
        self.load()
        
    def add_relation(self, entity1: str, relation: str, entity2: str):
        self.graph.add_edge(entity1, entity2, relation=relation)
        self.save()
        
    def get_relations(self, entity: str) -> list:
        if entity in self.graph:
            return list(self.graph.edges(entity, data=True))
        return []
        
    def save(self):
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        data = nx.node_link_data(self.graph)
        with open(self.filepath, 'w') as f:
            json.dump(data, f)
            
    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                self.graph = nx.node_link_graph(data)

knowledge_graph = KnowledgeGraph()
