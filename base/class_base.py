from __future__ import annotations
from base.field_base import FieldBase
from typing import TYPE_CHECKING
import jsonpickle
if TYPE_CHECKING:
    from base.model_base import ModelBase


class ClassBase:
    def __init__(self,
                 model_base: ModelBase,
                 reference_class: type,
                 count: int) -> None:
        self.model_base: ModelBase = model_base
        self.model_base.append_class(self)
        self.fields: list[FieldBase] = []
        # silly debuger behaviour - it's treated as class var.
        self.reference_class: type = reference_class
        self.instances = []
        self.count: int = count

    def get_seed(self):
        return self.model_base.seed

    def append_field(self, field: FieldBase):
        self.fields.append(field)

    def create_instance(self):
        new = self.reference_class()
        self.instances.append(new)
        return new

    def create_instances(self, n: int):
        new_insts = []
        for i in range(n):
            new_insts.append(self.create_instance())
        return new_insts

    def naive_fill_in_instances(self):
        for instance in self.instances:
            for field in self.fields:
                field.fill_in_field(instance)

    def json_dump(self):
        with open(f"{self.reference_class.__name__}.json", "w") as fw:
            fw.write(jsonpickle.encode(self.instances))
