from base.field_base import FieldBase
from typing import List
from base.class_base import ClassBase
import networkx as nx
import matplotlib.pyplot as plt
import json


class ModelBase():
    """Root class for defining generational meta-model
    and performing data generation
    """
    def __init__(self) -> None:
        self.classes: List[ClassBase] = []
        self.fields_graph = nx.DiGraph()
        self.reverse_topological_order: list[FieldBase] = []

    def append_class(self, class_base: ClassBase):
        """Adds ClassBase to model

        Args:
            class_base (ClassBase): ClassBase instance to add
        """
        self.classes.append(class_base)

    def create_instances(self):
        """Creates empty class instances for each ClassBase
        """
        for b_class in self.classes:
            b_class.create_instances(b_class.count)

    def map_field_graph_full(self):
        """Creates fields graph of all inter field relations to make generation possible

        Raises:
            Exception: If fields relations are not forming Directed Acyclic Graph (DAG)
        """
        self.fields_graph = nx.DiGraph()
        fields = self.get_all_fields()
        for field in fields:
            self.fields_graph.add_node(field.class_field_str(), field=field)
        for field in fields:
            for v_field in field.virtually_related_fields:
                self.fields_graph.add_edge(
                    field.class_field_str(), v_field.class_field_str())
            for chain in field.get_chains():
                current_field = field
                for i in range(len(chain)):
                    self.fields_graph.add_edge(
                        current_field.class_field_str(), chain[i].class_field_str())
                    current_field = chain[i]
        if not nx.is_directed_acyclic_graph(self.fields_graph):
            raise Exception(
                "Field relations do not form Directed Acyclic Graph (DAG), check if relations are not forming cycles.")
        topological_order = list(
            reversed(list(nx.topological_sort(self.fields_graph))))
        for field_key in topological_order:
            self.reverse_topological_order.append(
                self.fields_graph.nodes[field_key]['field'])

    def draw_field_graph(self):
        """Draws graph of inter-fileds relations 
        (provided it was generated map_field_graph_full)

        Uses matpliotlib to generate graph

        Usefull for debugging purposes
        """
        nx.draw(self.fields_graph, with_labels=True, font_weight='bold',
                node_size=200, node_color="#b5c6ff")
        plt.show()

    def print_generation_order(self):
        """Prints names of fileds in oder of data generation
        `order number: class_name.field_name`
        """
        for i, fb in enumerate(self.reverse_topological_order):
            print(f"{i+1}: {fb.class_field_str()}")

    def get_all_fields(self) -> List[FieldBase]:
        """Returns list of all FieldBases form all ClassBases

        Returns:
            List[FieldBase]: List of all FieldBases
        """
        fields = []
        for class_base in self.classes:
            for field_base in class_base.fields:
                fields.append(field_base)
        return fields

    def fill_in_instances(self):
        """Generatred data for each field in instance using reverse topological order
        """
        for field in self.reverse_topological_order:
            if field.generator is not None:
                for instance in field.class_base.instances:
                    field.fill_in_field(instance)

    def generate_data(self):
        """Uses meta-model to generate data as setup using ClassBases, FieldBases and chosen generators

        Equivalend of calling
        
        `create_instances()`

        `map_field_graph_full()`

        `fill_in_instances()`
        """
        self.create_instances()
        self.map_field_graph_full()
        self.fill_in_instances()
