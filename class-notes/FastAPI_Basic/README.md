# FastAPI Basic - GET aur POST Examples

Ye file mein simple GET aur POST examples hain jo beginner students ke liye samajhne mein aasan hain.

## 📁 Files

- **main.py** - Sab examples with full comments (Hinglish mein)

## 🚀 Chalane ka Tarika

### Step 1: FastAPI aur Uvicorn Install Karo
```bash
pip install fastapi uvicorn
```

### Step 2: Server Start Karo
```bash
uvicorn main:app --reload
```

### Step 3: Testing Karo
Browser mein jaao:
```
http://localhost:8000/docs
```

Wahan par ek interactive UI milega jahan se sab endpoints test kar sakte ho!

---

## 📝 Endpoints ke Examples

### GET Examples (Data Lena)

#### 1. Simple GET
```
GET http://localhost:8000/greet
Response: {"message": "Hello, World!"}
```

#### 2. GET with Path Parameter
```
GET http://localhost:8000/greet/Ali
Response: {"message": "Hello, Ali!", "name": "Ali"}
```

#### 3. GET with Query Parameters
```
GET http://localhost:8000/student?name=Fatima&subject=Math
Response: {
  "student_name": "Fatima",
  "subject": "Math",
  "message": "Fatima is studying Math"
}
```

#### 4. GET All Books
```
GET http://localhost:8000/books
Response: {"books": [], "total": 0}
```

#### 5. GET Specific Book
```
GET http://localhost:8000/books/0
Response: {"book": {...}, "id": 0}
```

#### 6. GET All Products
```
GET http://localhost:8000/products
Response: {
  "products": [
    {"id": 1, "name": "Laptop", "price": 50000},
    {"id": 2, "name": "Mouse", "price": 1500}
  ],
  "total": 2
}
```

### POST Examples (Data Bhejnaa)

#### 1. POST New Book
```
POST http://localhost:8000/books

Body (JSON):
{
  "title": "Python Basics",
  "author": "Ali Khan",
  "pages": 250
}

Response:
{
  "message": "Book added successfully!",
  "book": {
    "title": "Python Basics",
    "author": "Ali Khan",
    "pages": 250
  },
  "total_books": 1
}
```

#### 2. POST New Student
```
POST http://localhost:8000/students

Body (JSON):
{
  "name": "Ahmed",
  "age": 20,
  "class": "2nd Year"
}

Response:
{
  "status": "Student registered successfully!",
  "student": {
    "id": 1,
    "name": "Ahmed",
    "age": 20,
    "class": "2nd Year"
  },
  "message": "Ahmed has been added!"
}
```

#### 3. POST New Product
```
POST http://localhost:8000/products

Body (JSON):
{
  "name": "Monitor",
  "price": 15000
}

Response:
{
  "message": "Product added successfully!",
  "product": {
    "id": 4,
    "name": "Monitor",
    "price": 15000
  }
}
```

---

## 💡 Key Learning Points

### GET (Data Lena)
- Browser se direct link par jaao to GET request hota hai
- `/docs` se GET endpoints test kar sakte ho
- Query parameters: `?name=value&subject=value`
- Path parameters: `/endpoint/{id}`

### POST (Data Bhejnaa)
- Browser se seedha POST nahi kar sakte
- `/docs` se POST endpoints test kar sakte ho
- JSON body mein data bhejte ho
- Server us data ko store/process karega

---

## 🧪 /docs Interface Kaise Use Karo

1. Browser mein `http://localhost:8000/docs` kholo
2. Har endpoint ek card mein likha hota hai
3. Endpoint par click karo to expand hoga
4. "Try it out" button dabo
5. Input fields fill karo (POST ke liye body mein JSON)
6. "Execute" button dabo
7. Response dekh lo!

---

## 📚 Comments in Code

`main.py` mein sab kuch Hinglish mein explain hai:
- Har function ke upar description likhi hai
- `# ye kya hai` likha hai
- `# ye kya karega` likha hai

---

## ⚡ Tips

1. **GET** - Data fetch karne ke liye
2. **POST** - Naya data add karne ke liye
3. **Dictionaries** - `{"key": "value"}` JSON banate hain
4. **Lists** - `[]` mein multiple items store hote hain
5. **f-strings** - `f"{variable}"` se string mein variable insert kar sakte ho

---

## 🎯 Practice

Try karein:
1. ✅ `/docs` mein GET `/greet/YourName` test karo
2. ✅ POST `/books` se naya book add karo
3. ✅ Phir `/books` GET se dekho ke book add hua ya nahi
4. ✅ `/students` POST se student add karo
5. ✅ `/status` GET se overall status dekho

---

**Happy Learning! 🎉**
