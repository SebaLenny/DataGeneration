from base.generator_base import GeneratorBase
import numpy as np
import math


class UniformDistributionGen(GeneratorBase):
    def __init__(self,
                 blank_procentage: float,
                 min: float,
                 max: float,
                 decimanls: int = None) -> None:
        super().__init__(blank_procentage)
        self.min = min
        self.max = max
        self.decimals = decimanls

    def generate_data(self, related_fields_values: dict = {}):
        if np.random.rand() < self.blank_procentage:
            return None
        to_ret = np.random.uniform(min, max)
        if self.decimals is not None:
            to_ret = round(to_ret, self.decimals)
        return to_ret
