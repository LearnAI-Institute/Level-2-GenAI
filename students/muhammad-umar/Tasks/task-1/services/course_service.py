from database import courses

def assign_course(student_id: int, course_no: int, db):
    if student_id not in db["database"]["students"]:
        return "Student not found"
    
    if course_no not in courses:
        return "Course not found"
    
    for course in db["database"]["courses"].values():

        if course["student_id"] == student_id:
            return "Student already exist"
    
    course_data = courses[course_no]
    course_data = {
        "student_id": student_id,
        **course_data
    }

    db["database"]["courses"][db["course_id"]] = course_data
    db["course_id"] += 1
    return course_data

def get_all_courses(db):
    return list(db["database"]["courses"].values())

def get_one_course(student_id: int, db):
    for course in db["database"]["courses"].values():

        if course["student_id"] == student_id:
            return course
    
    return None

def update_course(student_id: int, course_no: int, db):
    if course_no not in courses:
        return "Course not found"

    for course_id, course in db["database"]["courses"].items():

        if course["student_id"] == student_id:

            course_data = courses[course_no]
            course_data = {
                "student_id": student_id,
                **course_data
            }
            db["database"]["courses"][course_id] = course_data

            return course_data
        
    return "Student not found"

def delete_course(student_id: int, db):
    for course_id, course in db["database"]["courses"].items():

        if course["student_id"] == student_id:
            return db["database"]["courses"].pop(course_id, None)

    return "Student not found"