def create_student(data, db):
    data["student_id"] = db["student_id"]
    db["database"]["students"][db["student_id"]] = data
    db["student_id"] += 1
    return data

def get_all(db):
    return list(db["database"]["students"].values())

def get_one(student_id, db):
    return db["database"]["students"].get(student_id)

def update_student(student_id: int, data, db):
    if student_id not in db["database"]["students"]:
        return None

    data["student_id"] = student_id
    db["database"]["students"][student_id] = data
    return data

def delete_student(student_id: int, db):
    if student_id not in db["database"]["students"]:
        return None
    
    delete_courses = []

    for course_id, course in db["database"]["courses"].items():

        if course["student_id"] == student_id:
            delete_courses.append(course_id)

    for course_id in delete_courses:
        db["database"]["courses"].pop(course_id)

    return db["database"]["students"].pop(student_id)