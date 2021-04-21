from base.field_base import FieldBase


class GeneratorBase():
    def __init__(self,
                 blank_procentage: float) -> None:
        self.blank_procentage: float = blank_procentage
        self.field_base: FieldBase = None

    def generate_data(self):
        pass
