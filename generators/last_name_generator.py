import numpy as np
from base.generator_base import GeneratorBase
from faker import Faker


class LastNameGenerator(GeneratorBase):
    def __init__(self,
                 blank_percentage: float = 0) -> None:
        super().__init__(blank_percentage)
        self.fake = Faker()

    def generate_data(self, related_fields_values: dict, instance=None):
        if np.random.rand() < self.blank_percentage:
            return None
        return self.fake.last_name()
