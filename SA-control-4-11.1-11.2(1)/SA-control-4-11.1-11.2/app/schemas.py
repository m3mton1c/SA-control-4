from pydantic import BaseModel, EmailStr, conint, constr
from typing import Optional

class User(BaseModel):
    username: str
    age: int
    email: EmailStr
    password: str
    phone: Optional[str] = "Unknown"


class ErrorResponse(BaseModel):
    error: str
    details: Optional[list] = None