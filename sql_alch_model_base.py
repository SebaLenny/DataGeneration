import jsonpickle
from generators.universal_function_generator import UniversalFunctionGenerator
from generators.company_name_generator import CompanyNameGenerator
from generators.date_generator import DateGenerator
from models.sqlalchemy_model_base import SqlAlchemyModelBase
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
from sqlalchemy import Column, String, Integer, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, session
from faker import Faker
import json
from sqlalchemy_serializer import SerializerMixin

base = declarative_base()


class Company(base, SerializerMixin):
    __tablename__ = "Company"
    company_id = Column(Integer, primary_key=True)
    name = Column(String)
    city = Column(String)
    street_address = Column(String)
    company_mission = Column(String)
    workers = relationship("Person", back_populates="company")


class Person(base, SerializerMixin):
    __tablename__ = "Person"
    person_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(DateTime)
    gender = Column(String)
    salary = Column(Float)
    cars = relationship("Car", back_populates="owner")
    company_id = Column(Integer, ForeignKey("Company.company_id"))
    company = relationship("Company", back_populates="workers")


class Car(base, SerializerMixin):
    __tablename__ = "Car"
    car_id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("Person.person_id"))
    owner = relationship("Person", back_populates="cars")
    production_date = Column(DateTime)
    brand = Column(String)


if __name__ == "__main__":
    # "docker-compose up" the docker-compose.yml file to start database
    fake = Faker()

    model = SqlAlchemyModelBase(dialect="postgresql",
                                database="datagen",
                                username="postgres",
                                password="superpass",
                                host="localhost",
                                port="5432",
                                declarative_base=base)

    # Company
    cb_company = ClassBase(model, Company, count=5)
    FieldBase(cb_company, CompanyNameGenerator(), "name")
    FieldBase(cb_company, UniversalFunctionGenerator(f=fake.city), "city")
    FieldBase(cb_company, UniversalFunctionGenerator(
        f=fake.street_address), "street_address")
    FieldBase(cb_company, UniversalFunctionGenerator(
        f=fake.paragraph, nb_sentences=5), "company_mission")

    # Person
    cb_person = ClassBase(model, Person, 1000)
    FieldBase(cb_person, FirstNameGenerator(),
              "first_name", related_fields=["gender"])
    FieldBase(cb_person, LastNameGenerator(), "last_name")
    FieldBase(cb_person, DateGenerator("-50y", "-18y"), "birth_date")
    FieldBase(cb_person, WeightedPickGenerator(
        choices=["Male", "Female"], weights=[0.4, 0.6]), "gender")
    FieldBase(
        cb_person, NormalDistributionGen(mean=3000, std=1500, decimals=2, blank_percentage=.15), "salary")
    p_cars = FieldBase(cb_person, None, "cars")
    FieldBase(cb_person, RandomRelationGen(
        cb_company), "company")

    # CAR
    cb_car = ClassBase(model, Car, 10000)
    FieldBase(cb_car, RandomRelationGen(
        cb_person, reverse_relation_field=p_cars), "owner")
    FieldBase(cb_car, WeightedPickGenerator(
        ["VW", "Audi", "Seat", "Skoda"]), "brand")
    FieldBase(cb_car, DateGenerator("-30y", "-5y"), "production_date")

    # model.create_instances()
    # model.map_field_graph()
    # model.fill_in_instances()
    # model.generate_data()
    # model.save_to_db()
    model.generate_data_batches(20)

    sess = model.SessionMaker()
    res = sess.query(Person).join(Person.cars).limit(1000).all()
    obj_list = []
    for sample in res:
        obj_list.append(sample.to_dict(
            rules=("-company.workers", "-cars.owner")))
    with open("output.json", "w") as fw:
        fw.write(jsonpickle.encode(obj_list))
