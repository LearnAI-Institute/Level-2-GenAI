fake_db = {
    "database": {
        "students": {},
        "courses": {},
        "attendance": [],
        "marks": []
    },
    "student_id": 1,
    "course_id": 1,
}

def get_db():
    return fake_db

courses = {
    1: {
        "course_name": "Python Basics",
        "duration": "2 months"
    },

    2: {
        "course_name": "Python Advanced",
        "duration": "3 months"
    },

    3: {
        "course_name": "Front-end Development",
        "duration": "4 months"
    },

    4: {
        "course_name": "Back-end Development",
        "duration": "4 months"
    }
}