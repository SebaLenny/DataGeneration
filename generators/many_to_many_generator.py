from numpy.core.defchararray import count
from base.generator_base import GeneratorBase
from base.field_base import FieldBase
from base.class_base import ClassBase
import numpy as np


class ManyToManyGenerator(GeneratorBase):
    def __init__(self,
                 count: int,
                 many_to_many_class_base: ClassBase,
                 to_class_base: ClassBase,
                 self_reference_field: FieldBase,
                 to_reference_field: FieldBase,
                 reverse_to_reference_field: FieldBase = None,
                 blank_percentage: float = 0) -> None:
        super().__init__(blank_percentage=blank_percentage)
        self.one_to_many_class_base = many_to_many_class_base
        self.count = count
        self.self_reference_field = self_reference_field
        self.to_reference_field = to_reference_field
        self.to_class_base = to_class_base
        self.reverse_to_reference_field = reverse_to_reference_field

    def generate_data(self, related_fields_values: dict, instance):
        if np.random.rand() < self.blank_percentage:
            return None
        samples_count = min(self.count, len(
            self.to_class_base.instances))
        random_samples = np.random.choice(self.to_class_base.instances,
                                          size=samples_count,
                                          replace=False)
        mm_instances = []
        for sample in random_samples:
            inst: object = self.one_to_many_class_base.reference_class()
            inst.__setattr__(self.self_reference_field.field, instance)
            inst.__setattr__(self.to_reference_field.field, sample)
            self.one_to_many_class_base.instances.append(inst)
            if self.reverse_to_reference_field is not None:
                rev_list = getattr(
                    sample, self.reverse_to_reference_field.field)
                rev_list.append(inst)
            mm_instances.append(inst)
        return mm_instances
