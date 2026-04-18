# ========================
# FastAPI - Basic Examples
# GET aur POST Methods
# ========================

# Step 1: FastAPI library import karein
# FastAPI ek web framework hai jo API banane mein madad karta hai
from fastapi import FastAPI

# Step 2: FastAPI ka instance banayein
# app object se hum routes (endpoints) define karte hain
app = FastAPI()

# ========================
# EXAMPLE 1: Simple GET Request
# ========================

# @app.get("/greet") - ye batlata hai ki ye endpoint GET method use karega
# URL: http://localhost:8000/greet
@app.get("/greet")
def greet():
    # Function jo response return karega
    # ye dictionary JSON format mein convert hoga aur client ko bhej diya jayega
    return {"message": "Hello, World!"}


# ========================
# EXAMPLE 2: GET with Path Parameter
# ========================

# {name} - ye path parameter hai, URL se value lega
# URL: http://localhost:8000/greet/Ali
@app.get("/greet/{name}")
def greet_person(name: str):
    # name parameter automatically URL se extract hoga
    # Example: /greet/Ali -> name = "Ali"
    return {
        "message": f"Hello, {name}!",
        "name": name
    }


# ========================
# EXAMPLE 3: GET with Query Parameter
# ========================

# Query parameter - URL ke baad ? ke baad likha jata hai
# URL: http://localhost:8000/student?name=Fatima&subject=Math
@app.get("/student")
def student_info(name: str, subject: str):
    # Query parameters automatically extract hote hain
    # name aur subject parameters hain
    return {
        "student_name": name,
        "subject": subject,
        "message": f"{name} is studying {subject}"
    }


# ========================
# EXAMPLE 4: In-memory Database (Storage)
# ========================

# Ye list memory mein sab books store karega
# Jab server band hoga to data delete ho jayega
books = []

# GET - Sab books dekho
# URL: http://localhost:8000/books
@app.get("/books")
def get_all_books():
    # books list ko JSON format mein return karo
    return {
        "books": books,
        "total": len(books)
    }


# GET - Specific book dekho (by index)
# URL: http://localhost:8000/books/0
@app.get("/books/{book_id}")
def get_book(book_id: int):
    # Check karo ki book_id valid hai ya nahi
    if 0 <= book_id < len(books):
        return {
            "book": books[book_id],
            "id": book_id
        }
    # Agar book nahi mila to error message bhejo
    return {"error": f"Book {book_id} not found"}


# ========================
# EXAMPLE 5: Simple POST Request
# ========================

# POST - Naya book add karo
# URL: http://localhost:8000/books (POST method se)
# Body mein JSON data bhejo
@app.post("/books")
def add_book(book: dict):
    # 'book: dict' ka matlab - client JSON data bhejega aur hum dict mein ले sakte hain
    # Example JSON:
    # {
    #   "title": "Python Basics",
    #   "author": "Ali Khan",
    #   "pages": 250
    # }

    # Naya book list mein add kar diin
    books.append(book)

    # Response bhejo ke book successfully add ho gaya
    return {
        "message": "Book added successfully!",
        "book": book,
        "total_books": len(books)
    }


# ========================
# EXAMPLE 6: POST with Additional Info
# ========================

# In-memory database for students
students = []

# GET - Sab students dekho
# URL: http://localhost:8000/students
@app.get("/students")
def get_students():
    return {
        "students": students,
        "total": len(students)
    }


# POST - Naya student add karo
# URL: http://localhost:8000/students (POST method se)
@app.post("/students")
def add_student(student: dict):
    # Student ke liye unique ID assign karo
    student["id"] = len(students) + 1

    # Student ko list mein add karo
    students.append(student)

    # Response mein confirmation aur student info bhejo
    return {
        "status": "Student registered successfully!",
        "student": student,
        "message": f"{student.get('name', 'Unknown')} has been added!"
    }


# ========================
# EXAMPLE 7: GET all + GET one
# ========================

# In-memory database for products
products = [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Mouse", "price": 1500},
    {"id": 3, "name": "Keyboard", "price": 3000}
]

# GET - Sab products dekho
# URL: http://localhost:8000/products
@app.get("/products")
def get_products():
    return {
        "products": products,
        "total": len(products)
    }


# GET - Ek specific product dekho by ID
# URL: http://localhost:8000/products/1
@app.get("/products/{product_id}")
def get_product(product_id: int):
    # Loop se product find karo
    for product in products:
        if product["id"] == product_id:
            return product

    # Product nahi mila to error return karo
    return {"error": f"Product with ID {product_id} not found"}


# POST - Naya product add karo
# URL: http://localhost:8000/products (POST method se)
@app.post("/products")
def add_product(product: dict):
    # Naya ID assign karo (last product ka ID + 1)
    product["id"] = len(products) + 1

    # Product ko list mein add karo
    products.append(product)

    return {
        "message": "Product added successfully!",
        "product": product
    }


# ========================
# EXAMPLE 8: Simple JSON Response
# ========================

# GET - Status check karo
# URL: http://localhost:8000/status
@app.get("/status")
def check_status():
    # Simple JSON response
    return {
        "status": "Server is running!",
        "total_books": len(books),
        "total_students": len(students),
        "total_products": len(products)
    }


# ========================
# YEH CHALANE KE LEYE:
# ========================
# 1. Terminal mein jao
# 2. Ye command likho:
#    uvicorn main:app --reload
#
# 3. Browser mein jaao:
#    http://localhost:8000/docs
#
# 4. Wahan sab endpoints dekh sakte ho aur test kar sakte ho!
# ========================
