from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    major: str
    skills: str


class JobCreate(BaseModel):
    title: str
    company: str
    location: str
    required_skills: str
    description: str