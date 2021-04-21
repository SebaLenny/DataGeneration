from typing import List


class DistributionBase():
    def generate_sample() -> float:
        pass

    def generate_samples(count: int) -> List[float]:
        """Generate list of samples from distribution

        Args:
            count (int): how many samples

        Returns:
            List[float]: list of generated samples
        """
        pass
