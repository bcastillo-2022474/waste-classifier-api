from pydantic import BaseModel, Field
class UserSignupDto(BaseModel):
    first_name: str = Field(..., title="First name")
    last_name: str = Field(..., title="Last name")
    email: str = Field(..., title="Email")
    password: str = Field(..., title="Password")