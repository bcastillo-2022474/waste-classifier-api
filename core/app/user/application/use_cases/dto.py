from pydantic import BaseModel, EmailStr

class UpdateUserDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None

class ChangePasswordDTO(BaseModel):
    current_password: str
    new_password: str