from typing import Optional
from pydantic import BaseModel, EmailStr, validator

class SignUpModel(BaseModel):
    name: str
    email: EmailStr  # Use EmailStr here
    password: str
    organization: Optional[str] = None

    @validator("email")
    def validate_email(cls, v):
        # This runs only if EmailStr parsing succeeded
        if not v or "@" not in v:
            raise ValueError("Provide a valid email address")
        return v

    @validator("password")
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        if not any(char.isdigit() for char in v):
            raise ValueError("Password must contain a number")
        if not any(char.isupper() for char in v):
            raise ValueError("Password must contain an uppercase letter")
        return v


class LoginModel(BaseModel):
    email: EmailStr
    password: str

    @validator("email")
    def validate_email(cls, v):
        # This runs only if EmailStr parsing succeeded
        if not v or "@" not in v:
            raise ValueError("Provide a valid email address")
        return v

    @validator("password")
    def password_strength(cls, v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v