class GeneratorBase():
    def __init__(self,
                 blank_percentage: float = 0) -> None:
        self.blank_percentage: float = blank_percentage

    def generate_data(self, related_fields_values: dict = {}, instance=None):
        return None
