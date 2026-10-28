from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True



class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None  


class ResumeResponse(BaseModel):

    id: int
    filename: str
    filepath: str

    email: Optional[str] = None
    phone: Optional[str] = None
    skills: Optional[str] = None
    projects: Optional[str] = None
    score: Optional[int] = None

    class Config:
        from_attributes = True     