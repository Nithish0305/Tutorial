import json

students = [
    {"id": 1, "name": "Alice", "age": 22},
    {"id": 2, "name": "Bob", "age": 20},
    {"id": 3, "name": "Charlie", "age": 23}
]

students_sorted = sorted(students, key = lambda x: x["age"])

with open("students.json","w") as f:
    json.dump(students_sorted,f,indent = 4)

print("Students saved to students.json")