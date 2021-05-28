from faker import Faker
from generators.universal_function_generator import UniversalFunctionGenerator
from generators.print_relations_generator import PrintRelationsGenerator
from base.generator_base import GeneratorBase
from generators.uniform_distribution_gen import UniformDistributionGen
from generators.random_relation_gen import RandomRelationGen
from base.field_base import FieldBase
from generators.normal_distribution_gen import NormalDistributionGen
from generators.first_name_generator import FirstNameGenerator
from generators.last_name_generator import LastNameGenerator
from generators.weighted_pick_generator import WeightedPickGenerator
from typing import ClassVar, List
from base.model_base import ModelBase
from base.class_base import ClassBase


class Person:
    def __init__(self) -> None:
        self.first_name: str = ""
        self.last_name: str = ""
        self.gender: str = ""
        self.salary: float = 0
        self.cars: list[Car] = []


class Car:
    def __init__(self) -> None:
        self.owner: Person = None
        self.brand: str = ""
        self.color: str = ""
        self.description: str = ""


if __name__ == "__main__":
    model = ModelBase()

    # Person
    cb_person = ClassBase(
        model_base=model, reference_class=Person, count=10)
    FieldBase(cb_person, FirstNameGenerator(),
              field="first_name", related_fields=["gender"])
    FieldBase(cb_person, UniversalFunctionGenerator(
        f=Faker().last_name), field="last_name")
    FieldBase(cb_person, WeightedPickGenerator(
        choices=["Male", "Female"], weights=[0.4, 0.6]), field="gender")
    FieldBase(
        cb_person, NormalDistributionGen(mean=3000, std=1500, decimals=2, blank_percentage=.15), "salary")
    p_cars = FieldBase(cb_person, None, field="cars")

    # CAR
    cb_car = ClassBase(model_base=model, reference_class=Car, count=100)
    FieldBase(cb_car, RandomRelationGen(
        cb_person, reverse_relation_field=p_cars), field="owner")
    FieldBase(cb_car, WeightedPickGenerator(
        ["VW", "Audi", "Seat", "Skoda"]), field="brand")
    FieldBase(cb_car, WeightedPickGenerator(
        ["Red", "Blue", "Yellow", "Green"]), field="color")
    FieldBase(cb_car, UniversalFunctionGenerator(
        f=Faker().paragraph, nb_sentences=5), "description")
    # FieldBase(cb_car, WeightedPickGenerator(
    #     ["Good", "Average", "Bad", "Junk"]), field="condition", related_fields=["owner.salary"])
    # FieldBase(cb_car, PrintRelationsGenerator(), field="signature", related_fields=[
    #           "owner.first_name", "owner.last_name"])

    model.create_instances()
    model.map_field_graph_full()
    model.draw_field_graph()
    model.print_rev_topological_order()
    model.fill_in_instances()
    # cb_car.json_dump_to_file("test1.json")
    print("")
