from base.field_base import FieldBase
from typing import List
from base.class_base import ClassBase
import networkx as nx
import matplotlib.pyplot as plt
import json


class ModelBase():
    def __init__(self) -> None:
        self.classes: List[ClassBase] = []
        self.fields_graph = nx.DiGraph()
        self.reverse_topological_order: list[FieldBase] = []
        self.seed: int = None

    def append_class(self, class_base: ClassBase):
        self.classes.append(class_base)

    def create_instances(self):
        for b_class in self.classes:
            b_class.create_instances(b_class.count)

    def map_field_graph(self):
        fields = self.get_all_fields()
        for field in fields:
            self.fields_graph.add_node(field.class_field_str(), field=field)
        for field in fields:
            for end_field in field.get_end_fields():
                self.fields_graph.add_edge(
                    field.class_field_str(), end_field.class_field_str())
        topological_order = list(
            reversed(list(nx.topological_sort(self.fields_graph))))
        for field_key in topological_order:
            self.reverse_topological_order.append(
                self.fields_graph.nodes[field_key]['field'])

    def draw_field_graph(self):
        nx.draw(self.fields_graph, with_labels=True, font_weight='bold',
                node_size=200, node_color="#b5c6ff")
        plt.show()

    def get_all_fields(self) -> List[FieldBase]:
        fields = []
        for class_base in self.classes:
            for field_base in class_base.fields:
                fields.append(field_base)
        return fields

    def fill_in_instances(self):
        for field in self.reverse_topological_order:
            for instance in field.class_base.instances:
                field.fill_in_field(instance)
