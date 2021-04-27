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
        self.licence_plate: str = ""

if __name__ == "__main__":
    model = ModelBase()

    # Person
    cb_person = ClassBase(model, Person, 10)
    FieldBase(cb_person, FirstNameGenerator(),
              "first_name", related_fields=["gender"])
    FieldBase(cb_person, LastNameGenerator(), "last_name")
    FieldBase(cb_person, WeightedPickGenerator(
        choices=["Male", "Female"], weights=[0.4, 0.6]), "gender")
    FieldBase(
        cb_person, NormalDistributionGen(mean=3000, std=1500, decimanls=2, blank_procentage=.15), "salary")
    p_cars = FieldBase(cb_person, None, "cars")

    # CAR
    cb_car = ClassBase(model, Car, 100)
    FieldBase(cb_car, RandomRelationGen(cb_person, reverse_relation_field=p_cars), "owner")
    FieldBase(cb_car, WeightedPickGenerator(["VW", "Audi", "Seat", "Skoda"]), "licence_plate")

    model.create_instances()
    model.map_field_graph()
    model.draw_field_graph()
    model.fill_in_instances()
    # cb_person.json_dump()
    print("")
