"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date

# ---------------- Student Management System Schemas ----------------

class Student(BaseModel):
    first_name: str = Field(..., description="Student first name")
    last_name: str = Field(..., description="Student last name")
    email: str = Field(..., description="Student email")
    roll_number: str = Field(..., description="Unique roll number")
    class_id: Optional[str] = Field(None, description="Assigned class ID")

class Classroom(BaseModel):
    name: str = Field(..., description="Class name, e.g., Grade 9")
    section: Optional[str] = Field(None, description="Section identifier, e.g., A/B")
    subject: Optional[str] = Field(None, description="Subject focus (optional)")
    teacher_name: Optional[str] = Field(None, description="Primary teacher name")
    academic_year: Optional[str] = Field(None, description="Academic year, e.g., 2025-26")

class Assignment(BaseModel):
    class_id: str = Field(..., description="Classroom ID this assignment belongs to")
    title: str = Field(..., description="Assignment title")
    description: Optional[str] = Field(None, description="Assignment details")
    due_date: Optional[date] = Field(None, description="Due date")
    max_score: float = Field(100, ge=0, description="Maximum score")

class Grade(BaseModel):
    student_id: str = Field(..., description="Student ID")
    assignment_id: str = Field(..., description="Assignment ID")
    score: float = Field(..., ge=0, description="Score achieved")
    max_score: Optional[float] = Field(None, ge=0, description="Max score if differs from assignment")
    remarks: Optional[str] = Field(None, description="Teacher remarks")

# ---------------- Example Schemas (left for reference) ----------------

class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
