from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from base.class_base import ClassBase
    from base.generator_base import GeneratorBase


class FieldBase():
    def __init__(self,
                 generator: GeneratorBase,
                 field: str) -> None:
        self.class_base: ClassBase
        self.generator: GeneratorBase = generator
        self.generator.field_base = self
        self.field: str = field

    def get_seed(self):
        return self.class_base.get_seed()

    def set_generator(self, generator: GeneratorBase):
        self.generator: GeneratorBase = generator
        self.generator.field_base = self

    def fill_in_field(self, obj):
        setattr(obj, self.field, self.generator.generate_data())
