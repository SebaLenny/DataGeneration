from base.field_base import FieldBase


class GeneratorBase():
    def __init__(self,
                 blank_procentage: float = 0) -> None:
        self.blank_procentage: float = blank_procentage

    def generate_data(self, related_fields_values: dict = {}, instance=None):
        return None
