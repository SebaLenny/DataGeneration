from base.generator_base import GeneratorBase
from base.class_base import ClassBase
import numpy as np
import random


class RandomRelationGen(GeneratorBase):
    def __init__(self,
                 blank_procentage: float,
                 related_class: ClassBase,
                 duplicate_check_chance: float = 1,
                 duplicate_repeats: int = 5) -> None:
        super().__init__(blank_procentage)
        self.related_class = related_class
        self.duplicate_check_chance: float = duplicate_check_chance
        self.duplicate_repeats = duplicate_repeats
        self.used_relations = {}

    def add_to_used(self, object):
        if object in self.used_relations:
            self.used_relations[object] += 1
        else:
            self.used_relations[object] = 1

    def generate_data(self):
        if np.random.rand() < self.blank_procentage:
            return None
        instances = self.related_class.instances
        check_chance = np.random.rand()
        for i in range(self.duplicate_repeats):
            random_instance = random.choice(instances)
            if check_chance < self.duplicate_check_chance:
                if random_instance not in self.used_relations:
                    self.add_to_used(random_instance)
                    return random_instance
            else:
                self.add_to_used(random_instance)
                return random_instance
        return None
