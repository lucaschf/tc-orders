from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from src.application.api.types import PydanticExternalEntityId, CPFStr
from src.application.use_cases.customer.create import (
    CustomerCreationDTO,
    CustomerCreatedDTO,
)
from src.domain.__shared.value_objects import CPF, EmailAddress


class BaseCustomer(BaseModel):
    """Base schema for customer data."""

    name: str = Field(
        description="The customer full name", min_length=3, max_length=100
    )
    email: EmailStr = Field(description="The customer email address")
    cpf: CPFStr = Field(description="The customer CPF number")


class CustomerSummaryOut(BaseCustomer):
    """Schema for returning a simplified customer."""

    pass


class CustomerCreationIn(BaseCustomer):
    """Schema for creating a new customer."""

    def to_customer_creation_data(self) -> CustomerCreationDTO:
        """Converts the schema into a CustomerData instance."""
        return CustomerCreationDTO(
            name=self.name,
            cpf=CPF(number=self.cpf),
            email=EmailAddress(address=str(self.email)),
        )

    model_config = ConfigDict(str_strip_whitespace=True)


class CustomerDetailsOut(CustomerSummaryOut):
    """Schema for returning a customer."""

    external_id: PydanticExternalEntityId = Field(
        description="The customer external id"
    )
    created_at: datetime = Field(description="The customer creation date")

    @staticmethod
    def from_dto(dto: CustomerCreatedDTO) -> "CustomerDetailsOut":
        return CustomerDetailsOut(
            name=dto.name,
            cpf=CPFStr(dto.cpf.number),
            email=dto.email.address,  # type: ignore
            external_id=PydanticExternalEntityId(dto.external_id),
            created_at=dto.created_at,
        )


__all__ = [
    "CustomerCreationIn",
    "CustomerDetailsOut",
    "CustomerSummaryOut",
]
