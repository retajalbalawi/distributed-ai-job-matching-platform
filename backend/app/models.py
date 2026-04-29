from sqlalchemy import Column, Integer, String, Float, Text
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    major = Column(String)
    skills = Column(Text)  # store as comma-separated for now


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    company = Column(String)
    location = Column(String)
    required_skills = Column(Text)
    description = Column(Text)


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    job_id = Column(Integer)
    score = Column(Float)
    explanation = Column(Text)
