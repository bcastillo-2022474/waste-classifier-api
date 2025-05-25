from pydantic import BaseModel, EmailStr

class UpdateUserDTO(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None