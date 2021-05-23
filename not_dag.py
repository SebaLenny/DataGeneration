from generators.uniform_distribution_gen import UniformDistributionGen
from generators.random_relation_gen import RandomRelationGen
from base.field_base import FieldBase
from generators.normal_distribution_gen import NormalDistributionGen
from generators.first_name_generator import FirstNameGenerator
from generators.last_name_generator import LastNameGenerator
from base.model_base import ModelBase
from base.class_base import ClassBase


class A:
    def __init__(self) -> None:
        self.alpha: str = ""
        self.beta: str = ""


if __name__ == "__main__":
    model = ModelBase()

    # Person
    cb_a = ClassBase(model, A, 10)
    FieldBase(cb_a, FirstNameGenerator(),
              "alpha", related_fields=["beta"])
    FieldBase(cb_a, FirstNameGenerator(),
              "beta", related_fields=["alpha"])


    model.create_instances()
    model.map_field_graph_full()
    model.draw_field_graph()
    model.fill_in_instances()
    print("")
