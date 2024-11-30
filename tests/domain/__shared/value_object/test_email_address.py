import pytest

from src.domain.__shared.value_objects import EmailAddress, InvalidEmailError


@pytest.mark.parametrize(
    "email",
    [
        "test@example.com",
        "firstname.lastname@domain.co.uk",
        "long.email+with+plus@subdomain.domain.com",
    ],
)
def test_valid_email_address(email: str) -> None:
    email_address = EmailAddress(address=email)
    assert email_address.address == email

    assert str(email_address) == email


# Test cases for invalid email addresses
@pytest.mark.parametrize(
    "email",
    [
        "invalid",
        "missing@domain",
        "@missing_local_part.com",
        "user@invalid..com",
        "user@domain.com.",
        "user@-domain.com",
    ],
)
def test_invalid_email_address(email: str) -> None:
    with pytest.raises(InvalidEmailError) as exc_info:
        EmailAddress(address=email)

    assert exc_info.value.message == "Endereço de e-mail inválido."
