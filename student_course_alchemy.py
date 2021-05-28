from numpy.core.defchararray import mod
from generators.many_to_many_generator import ManyToManyGenerator
import jsonpickle
from sqlalchemy.sql.sqltypes import REAL
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
import numpy as np

base = declarative_base()


class Student(base, SerializerMixin):
    __tablename__ = "Student"
    student_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    birth_date = Column(DateTime)
    gender = Column(String)
    enrolments = relationship("Enrolment", back_populates="student")


class Enrolment(base, SerializerMixin):
    __tablename__ = "Enrolment"
    enrolment_id = Column(Integer, primary_key=True)
    grade = Column(Float)
    student_id = Column(Integer, ForeignKey("Student.student_id"))
    student = relationship("Student", back_populates="enrolments")
    course_id = Column(Integer, ForeignKey("Course.course_id"))
    course = relationship("Course", back_populates="enrolees")


class Course(base, SerializerMixin):
    __tablename__ = "Course"
    course_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    ects_points = Column(Integer)
    enrolees = relationship("Enrolment", back_populates="course")


if __name__ == "__main__":
    # "docker-compose up" the docker-compose.yml file to start database
    fake = Faker()

    model = SqlAlchemyModelBase(dialect="postgresql",
                                database="university",
                                username="postgres",
                                password="superpass",
                                host="localhost",
                                port="5432",
                                declarative_base=base)

    # Student
    cb_student = ClassBase(model, reference_class=Student, count=5000)
    FieldBase(cb_student, FirstNameGenerator(),
              "first_name", related_fields=["gender"])
    FieldBase(cb_student, LastNameGenerator(), "last_name")
    FieldBase(cb_student, DateGenerator("-30y", "-18y"), "birth_date")
    FieldBase(cb_student, WeightedPickGenerator(
        choices=["Male", "Female"]), "gender")

    # Course
    cb_course = ClassBase(model, reference_class=Course, count=300)
    FieldBase(cb_course, UniversalFunctionGenerator(
        f=Faker().sentence, nb_words=2, variable_nb_words=False), "name")
    FieldBase(cb_course, UniversalFunctionGenerator(
        f=Faker().paragraph, nb_sentences=3), "description")
    ects_options = np.array([1, 3, 4, 5, 7, 13])
    weights = (1/ects_options)/np.sum(1/ects_options)
    FieldBase(cb_course, WeightedPickGenerator(
        list(ects_options), weights), "ects_points")
    fb_enrolees = FieldBase(cb_course, None, "enrolees")

    # Enrolment
    cb_enrolment = ClassBase(model, reference_class=Enrolment, count=0)
    fb_studnet = FieldBase(cb_enrolment, None, "studnet")
    fb_course = FieldBase(cb_enrolment, None, "course")

    # Student - enrolments
    fb_enrolments = FieldBase(cb_student, ManyToManyGenerator(one_to_many_class_base=cb_enrolment,
                                                              count=10,
                                                              self_reference_field=fb_studnet,
                                                              to_reference_field=fb_course,
                                                              to_class_base=cb_course,
                                                              reverse_to_reference_field=fb_enrolees), "enrolments")

    FieldBase(cb_enrolment,
              WeightedPickGenerator(
                  [2, 3, 3.5, 4, 4.5, 5, 5.5],
                  blank_percentage=.7),
              "grade", virtually_related_fields=[fb_enrolments])

    model.generate_data()
    model.draw_field_graph()
    model.print_rev_topological_order()
    # model.save_to_db()
    print("...")
