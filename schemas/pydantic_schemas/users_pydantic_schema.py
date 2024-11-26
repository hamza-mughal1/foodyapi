from pydantic import BaseModel, EmailStr, field_validator, FieldValidationInfo
import re


class CreateUser(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    
    @field_validator("password")
    def validate_password(cls, value: str, info: FieldValidationInfo):
        min = 8
        max = 15
        # Check for length between min and max characters
        if not min <= len(value) <= max:
            raise ValueError(f"Password must be between {min} and {max} characters.")

        # Check for at least one uppercase letter
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")

        # Check for at least one digit
        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")

        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValueError("Password must contain at least one special character.")
        
        return value