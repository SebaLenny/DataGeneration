from base.generator_base import GeneratorBase
import numpy as np


class WeightedPickGenerator(GeneratorBase):
    def __init__(self,
                 choices: list,
                 weights: list[float] = None,
                 blank_percentage: float = 0,
                 ) -> None:
        super().__init__(blank_percentage)
        self.choices = choices
        self.weights = weights

    def generate_data(self, related_fields_values: dict, instance=None):
        if np.random.rand() < self.blank_percentage:
            return None
        return np.random.choice(self.choices, p=self.weights).item()
