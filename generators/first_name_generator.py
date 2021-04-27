import numpy as np
from base.generator_base import GeneratorBase
from faker import Faker


class FirstNameGenerator(GeneratorBase):
    def __init__(self,
                 blank_procentage: float = 0) -> None:
        super().__init__(blank_procentage)
        self.fake = Faker()

    def generate_data(self, related_fields_values: dict, instance=None):
        if np.random.rand() < self.blank_procentage:
            return None
        _ = [x for x in related_fields_values.keys() if "gender" in x.lower()]
        if len(_) > 0:
            key = _[0]
            gender = related_fields_values[key].lower()
            if "male" == gender or "m" == gender:
                return self.fake.first_name_male()
            elif "female" == gender or "f" == gender:
                return self.fake.first_name_female()
            else:
                return self.fake.first_name()
        return self.fake.first_name()
