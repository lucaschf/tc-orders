from types import MappingProxyType

from pydantic_core import ErrorDetails

_CUSTOM_PYDANTIC_MESSAGES = MappingProxyType({
    "extra_forbidden": "Campo desconhecido",
    "too_short": "Deve possuir pelo menos {min_length} itens",
    "string_too_short": "Deve possuir pelo menos {min_length} caracteres",
    "missing": "Campo obrigatório",
    "string_type": "Deve ser uma string válida",
    "less_than_equal": "Deve ser menor ou igual a {le}",
    "less_than": "Deve ser menor que {lt}",
    "greater_than": "Deve ser maior que {gt}",
    "greater_than_equal": "Deve ser maior ou igual a {ge}",
    "enum": "Deve ser {expected}",
    "model_type": "Dados inválidos",
    "model_attributes_type": (
        "A entrada deve ser um dicionário ou objeto válido para extrair campos"
    ),
    "is_instance_of": "Deve ser uma instância de {class}",
    "dataclass_exact_type": "Deve ser uma instância de {class_name}",
    # Add more as needed. See https://docs.pydantic.dev/latest/errors/validation_errors/
})


def translate_pydantic_error_msg(error: ErrorDetails) -> str:
    """Translates a Pydantic error message to a more user-friendly format."""
    if custom_message := _CUSTOM_PYDANTIC_MESSAGES.get(error["type"]):
        ctx = error.get("ctx")
        if error["type"] == "too_short" and (ctx and ctx.get("min_length") == 1):
            custom_message = "Deve possuir pelo menos 1 item"

        return custom_message.format(**ctx) if ctx else custom_message

    if error.get("type") == "value_error":
        return error["msg"].replace("Value error, ", "")

    return error.get("msg")


__all__ = ["translate_pydantic_error_msg"]
