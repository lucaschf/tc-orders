import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True, slots=True)
class ValidationErrorDetails:
    loc: tuple[str | int, ...]
    msg: str

    def __str__(self) -> str:
        return json.dumps(asdict(self))

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"


__all__ = ["ValidationErrorDetails"]
