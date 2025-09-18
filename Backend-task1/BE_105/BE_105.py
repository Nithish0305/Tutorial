from fastapi import FastAPI,HTTPException

app = FastAPI()

students = [
    {"id": 1, "name": "Alice", "age": 22, "dept": "CSE"},
    {"id": 2, "name": "Bob", "age": 21, "dept": "ECE"},
    {"id": 3, "name": "Charlie", "age": 23, "dept": "IT"}
]

@app.get("/students")
def all_students():
    return students

@app.get("/students/{id}")
def particular_student(id: int):
    for i in students:
        if i["id"]==id:
            return i
    raise HTTPException(status_code = 404,detail = f"Student with ID: {id} not found.")
