import random


class CPFProvider:
    """A Brazilian CPF numbers provider."""

    # noinspection PyMethodMayBeStatic
    def cpf_number(self) -> str:
        """Return a random cpf number."""
        return self.generate_cpf_number()

    @classmethod
    def generate_cpf_number(cls) -> str:
        """Generate a valid CPF number."""
        # Initialize with 9 random digits
        cpf = [random.randint(0, 9) for _ in range(9)]  # noqa: S311

        # Calculate the first check digit
        digit1 = cls._calculate_check_digit(cpf, 10)
        cpf.append(digit1)

        # Calculate the second check digit
        digit2 = cls._calculate_check_digit(cpf, 11)
        cpf.append(digit2)

        # Format and return as string
        return "".join(map(str, cpf))

    @staticmethod
    def _calculate_check_digit(cpf_digits: list[int], multiplier_start: int) -> int:
        check_sum = sum(
            cpf_digits[i] * (multiplier_start - i) for i in range(len(cpf_digits))
        )
        remainder = check_sum % 11
        return 0 if remainder < 2 else 11 - remainder


__all__ = ["CPFProvider"]
