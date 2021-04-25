from __future__ import annotations
from typing import List, TYPE_CHECKING
import base
import operator
if TYPE_CHECKING:
    from base.relation_generator_base import RelationGeneratorBase
    from base.class_base import ClassBase
    from base.generator_base import GeneratorBase


class FieldBase():
    def __init__(self,
                 class_base: ClassBase,
                 generator: GeneratorBase,
                 field: str,
                 related_fields: list[str] = []) -> None:
        self.class_base: ClassBase = class_base
        self.class_base.append_field(self)
        self.generator: GeneratorBase = generator
        self.field: str = field
        self._related_fields = related_fields
        self._related_attrgetters = {}
        for relatd_field in self._related_fields:
            self._related_attrgetters[relatd_field] = operator.attrgetter(
                relatd_field)

    def get_seed(self):
        return self.class_base.get_seed()

    def get_end_fields(self) -> List[FieldBase]:
        end_fields = []
        for related_field in self._related_fields:
            end_fields.append(self._get_end_field(related_field))
        return end_fields

    def _get_end_field(self, related_field):
        split = related_field.split(".")
        class_base = self.class_base
        for split_field in split:
            field_base_find = [
                fb for fb in class_base.fields if fb.field == split_field]
            if len(field_base_find) < 1:
                raise Exception(
                    f"No field {split_field} found in {class_base.reference_class.__name__}\'s class base")
            field_base = field_base_find[0]
            if split_field == split[-1]:
                return field_base  # end field base found
            if not issubclass(field_base.generator.__class__, base.relation_generator_base.RelationGeneratorBase):
                raise Exception(
                    f"{split_field}\'s does not have generator of RelationGeneratorBase sublcass")
            class_base = field_base.generator.related_class

    def fill_in_field(self, instance):
        related_fields_values = {}
        for related_field in self._related_fields:
            try:
                related_fields_values[related_field] = self._related_attrgetters[related_field](
                    instance)
            except Exception:
                related_fields_values[related_field] = None
        setattr(instance, self.field,
                self.generator.generate_data(related_fields_values))

    def class_field_str(self):
        return f"{self.class_base.reference_class.__name__}.{self.field}"
