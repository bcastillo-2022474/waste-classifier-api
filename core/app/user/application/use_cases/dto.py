from pydantic import BaseModel, EmailStr, field_validator
from pydantic import BaseModel, validator

class UpdateUserDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None

class ChangePasswordDTO(BaseModel):
    current_password: str
    new_password: str

    @field_validator("current_password", "new_password")
    def not_none(cls, v, field):
        if v is None:
            raise ValueError(f"{field.name} cannot be None")
        if v.strip() == "":
            raise ValueError(f"{field.name} cannot be empty")
        return v