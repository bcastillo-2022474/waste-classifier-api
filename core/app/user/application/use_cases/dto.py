from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

class UpdateUserDTO(BaseModel):
    model_config = ConfigDict(
        # This excludes None values when converting to dict
        # Useful if you want to exclude unset fields
        exclude_none=True,
        # Validates assignment after object creation
        validate_assignment=True,
        # Allows extra fields to be ignored instead of raising error
        extra='ignore'
    )

    first_name: Optional[str] = Field(None, min_length=1, max_length=50)
    last_name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr] = None

    def has_updates(self) -> bool:
        """Check if any field has been set for update"""
        return any(getattr(self, field) is not None for field in self.model_fields)

class ChangePasswordDTO(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)