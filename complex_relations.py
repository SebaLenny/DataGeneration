from faker import Faker
from generators.uniform_distribution_gen import UniformDistributionGen
from generators.random_relation_gen import RandomRelationGen
from base.field_base import FieldBase
from generators.normal_distribution_gen import NormalDistributionGen
from generators.first_name_generator import FirstNameGenerator
from generators.last_name_generator import LastNameGenerator
from generators.universal_function_generator import UniversalFunctionGenerator
from generators.print_relations_generator import PrintRelationsGenerator
from base.model_base import ModelBase
from base.class_base import ClassBase


class A:
    def __init__(self) -> None:
        self.alpha: str = ""
        self.C: C = None


class B:
    def __init__(self) -> None:
        self.alpha: str = ""
        self.C: C = None


class C:
    def __init__(self) -> None:
        self.alpha: str = ""
        self.beta: str = ""
        self.gamma: str = ""
        self.delta: str = ""


if __name__ == "__main__":
    model = ModelBase()

    # Person
    cb_a = ClassBase(model, A, 10)
    cb_b = ClassBase(model, B, 10)
    cb_c = ClassBase(model, C, 10)

    FieldBase(cb_a, PrintRelationsGenerator(),
              "alpha", related_fields=["C.alpha", "C.beta", "C.gamma"])
    FieldBase(cb_a, RandomRelationGen(cb_c), "C")

    FieldBase(cb_b, PrintRelationsGenerator(),
              "alpha", related_fields=["C.alpha", "C.beta", "C.gamma"])
    FieldBase(cb_b, RandomRelationGen(cb_c), "C")

    FieldBase(cb_c, PrintRelationsGenerator(),
              "alpha", related_fields=["beta"])
    FieldBase(cb_c, PrintRelationsGenerator(),
              "beta", related_fields=["gamma"])
    FieldBase(cb_c, PrintRelationsGenerator(),
              "gamma", related_fields=["delta"])
    FieldBase(cb_c, UniversalFunctionGenerator(
        f=Faker().paragraph, nb_sentences=1),
        "delta")

    model.create_instances()
    model.map_field_graph_full()
    model.print_rev_topological_order()
    model.draw_field_graph()
    model.fill_in_instances()
    print("")
