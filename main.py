from generators.random_relation_gen import RandomRelationGen
from base.field_base import FieldBase
from generators.normal_distribution_gen import NormalDistributionGen
from typing import ClassVar, List
from base.model_base import ModelBase
from base.class_base import ClassBase


class Person:
    def __init__(self) -> None:
        self.first_name: float = 0
        self.salary: float = 0
        self.liked_cars: str = ""
        self.annual_salary: str = ""
        # self.cars: List[Car]


class Car:
    def __init__(self) -> None:
        self.name: str = ""
        self.condition: str = ""
        self.owner: Person = None


if __name__ == "__main__":
    model = ModelBase()

    # Person
    cb_person = ClassBase(model, Person, 10000)
    p_salary = FieldBase(
        cb_person, NormalDistributionGen(.1, 3000, 1500, 2), "salary")
    p_liked_cars = FieldBase(
        cb_person, NormalDistributionGen(.1, 3000, 1500, 2), "liked_cars")
    p_annual_salary = FieldBase(
        cb_person, NormalDistributionGen(.1, 30000, 15000, 2), "annual_salary", related_fields=["salary"])

    # Car
    cb_car = ClassBase(model, Car, 15000)
    c_owner = FieldBase(cb_car, RandomRelationGen(.1, cb_person, .25), "owner")
    c_condition = FieldBase(cb_car, RandomRelationGen(.1, cb_person, .25),
                            "condition", related_fields=["owner.liked_cars", "owner.salary"])

    model.create_instances()
    model.map_field_graph()
    model.draw_field_graph()
    cb_car.naive_fill_in_instances()
    cb_person.naive_fill_in_instances()
    print("")
