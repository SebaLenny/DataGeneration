import numpy as np
from base.generator_base import GeneratorBase
from faker import Faker


class FirstNameGenerator(GeneratorBase):
    def __init__(self,
                 blank_percentage: float = 0) -> None:
        super().__init__(blank_percentage)
        self.fake = Faker()

    def generate_data(self, related_fields_values: dict, instance=None):
        if np.random.rand() < self.blank_percentage:
            return None
        fields_with_gender = [x for x in related_fields_values.keys() if "gender" in x.lower()]
        if len(fields_with_gender) > 0:
            key = fields_with_gender[0]
            gender = related_fields_values[key].lower()
            if "male" == gender or "m" == gender:
                return self.fake.first_name_male()
            elif "female" == gender or "f" == gender:
                return self.fake.first_name_female()
        return self.fake.first_name()
