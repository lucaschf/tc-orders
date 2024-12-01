from typing import Dict

import pytest
from pydantic import BaseModel

from src.application.api.types.cpf_str import CPFStr

valid_cpfs = [
    {"masked": "987.471.450-64", "plain": "98747145064"},
    {"masked": "223.837.100-16", "plain": "22383710016"},
    {"masked": "411.278.860-61", "plain": "41127886061"},
    {"masked": "108.564.466-96", "plain": "10856446696"},
    {"masked": "474.465.470-30", "plain": "47446547030"},
    {"masked": "376.261.690-69", "plain": "37626169069"},
    {"masked": "300.972.750-00", "plain": "30097275000"},
    {"masked": "354.735.600-83", "plain": "35473560083"},
    {"masked": "251.462.470-30", "plain": "25146247030"},
    {"masked": "615.337.140-02", "plain": "61533714002"},
]

invalid_cpfs = [
    "12345678901",
    "123.456.789-01",
    "108a564b466c96",
    "random_string",
    "11111111111",
    "aaa.bbb.ccc=dd",
]


class PersonTestModel(BaseModel):
    """A Pydantic model for testing CPF validation."""

    cpf: CPFStr


@pytest.mark.parametrize("input_data", valid_cpfs)
def test_valid_cpfs(input_data: Dict[str, str]) -> None:
    """Test valid CPFs.

    Args:
        input_data (dict[str, str]): A dictionary containing masked and plain CPF strings.

    Returns:
        None
    """
    cpf: CPFStr = CPFStr(input_data.get("masked"))
    assert cpf == input_data.get("plain")


@pytest.mark.parametrize("invalid_cpf", invalid_cpfs)
def test_invalid_cpf(invalid_cpf: str) -> None:
    """Test invalid CPFs.

    Args:
        invalid_cpf (str): An invalid CPF string.

    Returns:
        None
    """
    with pytest.raises(ValueError):
        CPFStr(invalid_cpf)


@pytest.mark.parametrize("input_data", valid_cpfs)
def test_valid_cpfs_model(input_data: Dict[str, str]) -> None:
    """Test valid CPFs using the PersonTestModel.

    Args:
        input_data (dict[str, str]): A dictionary containing masked and plain CPF strings.

    Returns:
        None
    """
    person = PersonTestModel(cpf=CPFStr(input_data.get("masked")))
    assert person.cpf == input_data.get("plain")


@pytest.mark.parametrize("invalid_cpf", invalid_cpfs)
def test_invalid_cpf_model(invalid_cpf: str) -> None:
    """Test invalid CPFs using the PersonTestModel.

    Args:
        invalid_cpf (str): An invalid CPF string.

    Returns:
        None
    """
    with pytest.raises(ValueError):
        PersonTestModel(cpf=CPFStr(invalid_cpf))


def test_cpf_str_pydantic_json_schema() -> None:
    def mock_handler(_):  # noqa: ANN001, ANN202
        return {}

    schema = CPFStr.__get_pydantic_core_schema__()
    json_schema = CPFStr.__get_pydantic_json_schema__(
        schema,
        mock_handler,  # type: ignore
    )

    assert "example" in json_schema
    example_cpf_number = json_schema["example"]
    assert CPFStr._validate_and_remove_mask(example_cpf_number) == example_cpf_number
