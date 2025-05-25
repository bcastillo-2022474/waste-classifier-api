from pydantic import BaseModel, Field, EmailStr
class UserSignupDto(BaseModel):
    first_name: str = Field(..., title="First name")
    last_name: str = Field(..., title="Last name")
    email: EmailStr = Field(..., title="Email")
    password: str = Field(..., title="Password")