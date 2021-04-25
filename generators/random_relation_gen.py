from base.relation_generator_base import RelationGeneratorBase
from base.class_base import ClassBase
import numpy as np
import random


class RandomRelationGen(RelationGeneratorBase):
    def __init__(self,
                 related_class: ClassBase,
                 blank_procentage: float = 0,
                 duplicate_check_chance: float = 1,
                 duplicate_repeats: int = 5) -> None:
        super().__init__(blank_procentage, related_class)
        self.duplicate_check_chance: float = duplicate_check_chance
        self.duplicate_repeats = duplicate_repeats
        self.used_relations = {}

    def add_to_used(self, object):
        if object in self.used_relations:
            self.used_relations[object] += 1
        else:
            self.used_relations[object] = 1

    def generate_data(self, related_fields_values: dict = {}):
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
