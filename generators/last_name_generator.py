import numpy as np
from base.generator_base import GeneratorBase
from faker import Faker


class LastNameGenerator(GeneratorBase):
    def __init__(self,
                 blank_procentage: float = 0) -> None:
        super().__init__(blank_procentage)
        self.fake = Faker()

    def generate_data(self, related_fields_values: dict):
        if np.random.rand() < self.blank_procentage:
            return None
        return self.fake.last_name()