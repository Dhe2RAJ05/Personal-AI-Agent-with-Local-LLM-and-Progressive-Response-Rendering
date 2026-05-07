from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from backend.db.database import Base


# User table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# Integrations table (Gmail / Calendar tokens)
class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String, nullable=False)   # gmail, calendar
    access_token = Column(Text, nullable=False)
    refresh_token = Column(Text, nullable=True)
    token_expiry = Column(String, nullable=True)
    status = Column(String, default="active")


# Task logs table
class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String, nullable=False)
    task = Column(Text, nullable=False)
    status = Column(String, default="pending")   # pending, success, failed
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)