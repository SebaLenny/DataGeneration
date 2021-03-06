from exrex import generate
from base.generator_base import GeneratorBase
import exrex
import numpy as np


class RegexGenerator(GeneratorBase):
    def __init__(self,
                 regex: str,
                 blank_percentage: float = 0
                 ) -> None:
        super().__init__(blank_percentage)
        self.regex = regex

    def generate_data(self, related_fields_values: dict, instance=None):
        if np.random.rand() < self.blank_percentage:
            return None
        return exrex.getone(self.regex)
