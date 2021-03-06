import numpy as np
from base.generator_base import GeneratorBase


class UniversalFunctionGenerator(GeneratorBase):
    def __init__(self,
                 f,
                 blank_percentage: float = 0,
                 **kwargs,) -> None:
        super().__init__(blank_percentage)
        self.f = f
        self.kwargs = kwargs

    def generate_data(self, related_fields_values: dict, instance=None):
        if np.random.rand() < self.blank_percentage:
            return None
        return self.f(**self.kwargs)
