from base.sqlalchemy_class_base import SqlAlchemyModelBase
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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

base = declarative_base()


class Person(base):
    __tablename__ = "Person"
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    gender = Column(String)
    salary = Column(Float)
    cars = relationship("Car", back_populates="owner")


class Car(base):
    __tablename__ = "Car"
    car_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("Person.person_id"))
    owner = relationship("Person", back_populates="cars")
    brand = Column(String)


if __name__ == "__main__":
    model = SqlAlchemyModelBase(dialect="postgresql",
                                database="datagen",
                                username="postgres",
                                password="superpass",
                                host="localhost",
                                port="5432",
                                declarative_base=base)

    # Person
    cb_person = ClassBase(model, Person, 10000)
    FieldBase(cb_person, FirstNameGenerator(),
              "first_name", related_fields=["gender"])
    FieldBase(cb_person, LastNameGenerator(), "last_name")
    FieldBase(cb_person, WeightedPickGenerator(
        choices=["Male", "Female"], weights=[0.4, 0.6]), "gender")
    FieldBase(
        cb_person, NormalDistributionGen(mean=3000, std=1500, decimanls=2, blank_procentage=.15), "salary")
    p_cars = FieldBase(cb_person, None, "cars")

    # CAR
    cb_car = ClassBase(model, Car, 100000)
    FieldBase(cb_car, RandomRelationGen(
        cb_person, reverse_relation_field=p_cars), "owner")
    FieldBase(cb_car, WeightedPickGenerator(
        ["VW", "Audi", "Seat", "Skoda"]), "brand")

    model.create_instances()
    model.map_field_graph()
    model.draw_field_graph()
    model.fill_in_instances()
    model.save_to_db()
    print("")
