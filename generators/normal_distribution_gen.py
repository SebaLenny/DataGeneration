from base.generator_base import GeneratorBase
import numpy as np


class NormalDistributionGen(GeneratorBase):
    def __init__(self,
                 blank_procentage: float,
                 mean: float,
                 std: float,
                 decimanls: int = None) -> None:
        super().__init__(blank_procentage)
        self.mean = mean
        self.std = std
        self.decimals = decimanls

    def generate_data(self, related_fields_values: dict = {}):
        if np.random.rand() < self.blank_procentage:
            return None
        to_ret = np.random.normal(self.mean, self.std)
        if self.decimals is not None:
            to_ret = round(to_ret, self.decimals)
        return to_ret
