from typing import List
from base.class_base import ClassBase


class ModelBase():
    def __init__(self) -> None:
        self.classes: List[ClassBase] = []
        self.seed: int = None

    def append_class(self, class_base: ClassBase):
        class_base.model_base = self
        self.classes.append(class_base)

    def create_instances(self):
        for b_class in self.classes:
            b_class.create_instances(b_class.count)
