from base.field_base import FieldBase
from generators.first_name_generator import FirstNameGenerator
from generators.last_name_generator import LastNameGenerator
from generators.weighted_pick_generator import WeightedPickGenerator
from generators.normal_distribution_gen import NormalDistributionGen
from typing import List
from base.model_base import ModelBase
from base.class_base import ClassBase
from flask import Flask


class Person:
    def __init__(self) -> None:
        self.first_name: str = ""
        self.last_name: str = ""
        self.gender: str = ""
        self.salary: float = 0


app = Flask("__name__")


@app.route("/people/<N>")
def generate_people(N: str):
    model = ModelBase()

    # Person
    cb_person = ClassBase(model, Person, int(N))
    FieldBase(cb_person, FirstNameGenerator(),
              "first_name", related_fields=["gender"])
    FieldBase(cb_person, LastNameGenerator(), "last_name")
    FieldBase(cb_person, WeightedPickGenerator(
        choices=["Male", "Female"], weights=[0.4, 0.6]), "gender")
    FieldBase(cb_person, NormalDistributionGen(
        mean=5000, std=1000, decimals=2), "salary")

    model.create_instances()
    model.map_field_graph_full()
    # model.draw_field_graph()
    model.fill_in_instances()

    return cb_person.json_dump()
