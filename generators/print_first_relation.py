import numpy as np
from base.generator_base import GeneratorBase


class PrintFirstRelation(GeneratorBase):
    def __init__(self,
                 blank_percentage: float = 0) -> None:
        super().__init__(blank_percentage)

    def generate_data(self, related_fields_values: dict, instance=None):
        if np.random.rand() < self.blank_percentage:
            return None
        return next(iter(related_fields_values.values()))
