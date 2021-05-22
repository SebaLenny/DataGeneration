from base.generator_base import GeneratorBase
from base.class_base import ClassBase


class RelationGeneratorBase(GeneratorBase):
    def __init__(self,
                 blank_procentage: float,
                 related_class: ClassBase) -> None:
        super().__init__(blank_procentage)
        self.related_class: ClassBase = related_class
