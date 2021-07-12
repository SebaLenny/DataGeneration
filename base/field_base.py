from __future__ import annotations
from typing import List, TYPE_CHECKING
import generators
import operator
if TYPE_CHECKING:
    from generators.relation_generator_base import RelationGeneratorBase
    from base.class_base import ClassBase
    from base.generator_base import GeneratorBase


class FieldBase():
    """Relates to the field of class to generate data to.
    Is responsible for generating data using specified Generator
    """
    def __init__(self,
                 class_base: ClassBase,
                 generator: GeneratorBase,
                 field: str,
                 related_fields: list[str] = [],
                 virtually_related_fields: list[FieldBase] = []) -> None:
        """Init

        Args:
            class_base (ClassBase): Reference to ClassBase
            generator (GeneratorBase): Generator used for generating data
            field (str): string name of field to generate data to
            related_fields (list[str], optional): [description]. Defaults to []. List of related fields to be supplied to generator during data generation.
            Using string notation form the context of current class.
            virtually_related_fields (list[FieldBase], optional): [description]. Defaults to []. List of related FieldBases (only for organisational purposes).
        """
        self.class_base: ClassBase = class_base
        self.class_base.append_field(self)
        self.generator: GeneratorBase = generator
        self.field: str = field
        self._related_fields = related_fields
        self._related_attrgetters = {}
        for relatd_field in self._related_fields:
            self._related_attrgetters[relatd_field] = operator.attrgetter(
                relatd_field)
        self.virtually_related_fields = virtually_related_fields

    def get_end_fields(self) -> List[FieldBase]:
        """Returns list of FieldBases from related_fields

        Returns:
            List[FieldBase]: List of FiledBases
        """
        end_fields = []
        for related_field in self._related_fields:
            field = self._get_fields_chain(related_field)[-1]
            end_fields.append(field)
        return end_fields
    
    def get_chains(self) -> List[List[FieldBase]]:
        """Returns list of FieldBases chains that lead to related_fields

        Returns:
            List[FieldBase]: List of FiledBases
        """
        chains = []
        for related_field in self._related_fields:
            chains.append(self._get_fields_chain(related_field))
        return chains

    def _get_fields_chain(self, related_field) -> List[FieldBase]:
        split = related_field.split(".")
        class_base = self.class_base
        fields_chain = []
        for split_field in split:
            field_base_find = [
                fb for fb in class_base.fields if fb.field == split_field]
            if len(field_base_find) < 1:
                raise Exception(
                    f"No field {split_field} found in {class_base.reference_class.__name__}\'s class base")
            field_base = field_base_find[0]
            if split_field == split[-1]:
                fields_chain.append(field_base)
                return fields_chain  # end field base found
            if not issubclass(field_base.generator.__class__, generators.relation_generator_base.RelationGeneratorBase):
                raise Exception(
                    f"{split_field}\'s does not have generator of RelationGeneratorBase sublcass")
            fields_chain.append(field_base)
            class_base = field_base.generator.related_class

    def fill_in_field(self, instance):
        """Uses generator to generate data into field of specified instance

        Args:
            instance ([type]): Instace of class of filed
        """
        if self.generator is None:
            return
        related_fields_values = {}
        for related_field in self._related_fields:
            try:
                related_fields_values[related_field] = self._related_attrgetters[related_field](
                    instance)
            except Exception:
                related_fields_values[related_field] = None
        setattr(instance, self.field, self._prepare_field_value(
            related_fields_values, instance))

    def _prepare_field_value(self, related_fields_values, instance):
        return self.generator.generate_data(related_fields_values, instance=instance)

    def class_field_str(self) -> str:
        """Returns string of format `class_name.field_name`

        Returns:
            str: String of format `class_name.field_name`
        """
        return f"{self.class_base.reference_class.__name__}.{self.field}"
