from base.field_base import FieldBase
from typing import List
from base.class_base import ClassBase
import networkx as nx
import matplotlib.pyplot as plt


class ModelBase():
    def __init__(self) -> None:
        self.classes: List[ClassBase] = []
        self._fields_graph = nx.DiGraph()
        self.seed: int = None

    def append_class(self, class_base: ClassBase):
        self.classes.append(class_base)

    def create_instances(self):
        for b_class in self.classes:
            b_class.create_instances(b_class.count)

    def map_field_graph(self):
        fields = self.get_all_fields()
        for field in fields:
            self._fields_graph.add_node(field.class_field_str(), field=field)
        for field in fields:
            for end_field in field.get_end_fields():
                self._fields_graph.add_edge(
                    field.class_field_str(), end_field.class_field_str())

    def draw_field_graph(self):
        print(list(reversed(list(nx.topological_sort(self._fields_graph)))))
        nx.draw(self._fields_graph, with_labels=True, font_weight='bold',
                node_size=200, node_color="#b5c6ff")
        plt.show()

    def get_all_fields(self) -> List[FieldBase]:
        fields = []
        for class_base in self.classes:
            for field_base in class_base.fields:
                fields.append(field_base)
        return fields
