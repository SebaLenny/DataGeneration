import numpy as np
from base.generator_base import GeneratorBase
from faker import Faker


class DateGenerator(GeneratorBase):
    def __init__(self,
                 start_date,
                 end_date,
                 blank_percentage: float = 0,) -> None:
        super().__init__(blank_percentage)
        self.fake = Faker()
        self.start_date = start_date
        self.end_date = end_date

    def generate_data(self, related_fields_values: dict, instance=None):
        if np.random.rand() < self.blank_percentage:
            return None
        return self.fake.date_between(start_date=self.start_date, end_date=self.end_date)
