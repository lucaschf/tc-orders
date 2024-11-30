import pytest

from src.domain.__shared.value_objects import CPF, InvalidCPFError


def test_clean_cpf() -> None:
    dirty_cpf = "123.456.789-09"
    clean_cpf = "12345678909"
    assert CPF._clean_cpf(dirty_cpf) == clean_cpf


@pytest.mark.parametrize(
    "informed_cpf, expected",
    [
        ("108.564.466-96", "10856446696"),
        ("248.993.065-63", "24899306563"),
        ("162.138.995-29", "16213899529"),
        ("502.808.986-81", "50280898681"),
        ("683.298.145-72", "68329814572"),
        ("550.330.753-49", "55033075349"),
        ("582.968.396-28", "58296839628"),
        ("648.630.858-34", "64863085834"),
        ("674.285.998-90", "67428599890"),
        ("916.372.848-61", "91637284861"),
        ("427.385.946-70", "42738594670"),
        ("112.415.075-70", "11241507570"),
        ("751.513.007-50", "75151300750"),
        ("730.745.733-41", "73074573341"),
        ("869.362.916-60", "86936291660"),
        ("071.006.981-20", "07100698120"),
        ("778.468.794-05", "77846879405"),
    ],
)
def test_creation_of_valid_cpf(informed_cpf: str, expected: str) -> None:
    cpf = CPF(number=informed_cpf)
    assert cpf.number == expected


@pytest.mark.parametrize(
    "invalid_cpf",
    [
        "1234567890",  # CPF with less than 11 digits
        "..-10856446696",  # Malformed
        "...10856446696",  # Malformed
        "---10856446696",  # Malformed
        "1.08.564466-96",  # Malformed
        "108.564.466--96",  # Malformed
        "1234567890a",  # CPF with letters
        "11111111111",  # CPF with all digits equal
        "12345678901",  # CPF with an invalid check digit
    ],
)
def test_creation_of_invalid_cpf(invalid_cpf: str) -> None:
    with pytest.raises(InvalidCPFError) as exc_info:
        CPF(number=invalid_cpf)

    assert exc_info.value.cpf == invalid_cpf


@pytest.mark.parametrize(
    "cpf_number, expected",
    [
        ("108.564.466-96", "10856446696"),
        ("24899306563", "24899306563"),
    ],
)
def test_str(cpf_number: str, expected: str) -> None:
    cpf = CPF(number=cpf_number)
    assert str(cpf) == expected
