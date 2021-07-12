from __future__ import annotations
from base.field_base import FieldBase
from typing import TYPE_CHECKING
import jsonpickle
if TYPE_CHECKING:
    from base.model_base import ModelBase


class ClassBase:
    """Class for describing class of model that need to be generated.
    Responsible for generating instances of classes and agregates FieldBases
    """
    def __init__(self,
                 model_base: ModelBase,
                 reference_class: type,
                 count: int) -> None:
        """Init

        Args:
            model_base (ModelBase): Reference to ModelBase
            reference_class (type): Referecne to Class that neeeds to be generated
            count (int): How many instances should be generated during instance generation
        """
        self.model_base: ModelBase = model_base
        self.model_base.append_class(self)
        self.fields: list[FieldBase] = []
        # silly debuger behaviour - it's treated as class var.
        self.reference_class: type = reference_class
        self.instances = []
        self.count: int = count

    def append_field(self, field: FieldBase):
        """Adds FieldBase to class

        Args:
            field (FieldBase): FieldBase that needs to be added
        """
        self.fields.append(field)

    def create_instance(self):
        """Creates instance of referenced Class

        Returns:
            [type]: Created instance
        """
        new = self.reference_class()
        self.instances.append(new)
        return new

    def create_instances(self, n: int):
        """Creates n instances of referenced Class

        Args:
            n (int): Ammount of instances to be created

        Returns:
            [type]: Created instances
        """
        new_insts = []
        for i in range(n):
            new_insts.append(self.create_instance())
        return new_insts

    def json_dump(self):
        """Naively turns instaces into jsonpickle

        Returns:
            [type]: JSON formatted list of instances
        """
        return jsonpickle.encode(self.instances)

    def json_dump_to_file(self, output: str):
        """Saves naively jsonpickled instances into file

        Args:
            output (str): "Path of saved file"
        """
        if output is None:
            output = f"{self.reference_class.__name__}.json"
        with open(output, "w") as fw:
            fw.write(self.json_dump())

    def clear_instances(self):
        """Wipes out all created instances
        """
        self.instances = []
