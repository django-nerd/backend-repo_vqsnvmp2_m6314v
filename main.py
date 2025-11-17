import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Any
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Student, Classroom, Assignment, Grade

app = FastAPI(title="Student Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Helpers
class ObjectIdModel(BaseModel):
    id: str


def oid(id_str: str) -> ObjectId:
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ID")


@app.get("/")
def read_root():
    return {"message": "Student Management System API"}


@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Connected & Working"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    return response


# -------- Students --------
@app.post("/students", response_model=ObjectIdModel)
def create_student(student: Student):
    new_id = create_document("student", student)
    return {"id": new_id}


@app.get("/students")
def list_students():
    docs = get_documents("student")
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


# -------- Classrooms --------
@app.post("/classrooms", response_model=ObjectIdModel)
def create_classroom(classroom: Classroom):
    new_id = create_document("classroom", classroom)
    return {"id": new_id}


@app.get("/classrooms")
def list_classrooms():
    docs = get_documents("classroom")
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


# -------- Assignments --------
@app.post("/assignments", response_model=ObjectIdModel)
def create_assignment(assignment: Assignment):
    new_id = create_document("assignment", assignment)
    return {"id": new_id}


@app.get("/assignments")
def list_assignments(class_id: Optional[str] = None):
    filt = {"class_id": class_id} if class_id else {}
    docs = get_documents("assignment", filt)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


# -------- Grades / Marking --------
@app.post("/grades", response_model=ObjectIdModel)
def create_grade(grade: Grade):
    new_id = create_document("grade", grade)
    return {"id": new_id}


@app.get("/grades")
def list_grades(student_id: Optional[str] = None, assignment_id: Optional[str] = None):
    filt = {}
    if student_id:
        filt["student_id"] = student_id
    if assignment_id:
        filt["assignment_id"] = assignment_id
    docs = get_documents("grade", filt)
    for d in docs:
        d["id"] = str(d.pop("_id"))
    return docs


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
