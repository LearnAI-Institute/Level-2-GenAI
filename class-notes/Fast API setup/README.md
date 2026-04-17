# 🚀 FastAPI Setup - Beginner Friendly Materials

Complete guide to help beginners install FastAPI and create their first "Hello World" API.

---

## 📁 Files in This Folder

### 1. **FastAPI_Beginners_Setup_Guide.md** ⭐ (Start Here!)
Complete step-by-step guide with:
- How to check if Python is installed
- Creating a virtual environment
- Installing FastAPI
- Creating your first program
- Running it on a local server
- Accessing it in your browser
- Common problems and solutions
- Next steps and modifications

**Read this first if you are completely new to FastAPI!**

---

### 2. **Quick_Command_Reference.md** 
Quick reference with just the commands to copy-paste:
- All commands in order
- Code templates to try
- Common errors and fixes
- Checklist for success

**Use this when you just want the commands quickly!**

---

### 3. **main_template.py**
A ready-to-use Python template file with:
- Basic "Hello World" program
- Comments explaining each line
- 4 different modifications you can try
- Instructions for each modification

**Copy this code into your `main.py` file!**

---

## 🎯 How to Use These Files

### For Complete Beginners:

1. **Read:** `FastAPI_Beginners_Setup_Guide.md` (read all steps carefully)
2. **Copy:** Code from `main_template.py` into your `main.py` file
3. **Follow:** Commands from `Quick_Command_Reference.md`
4. **Run:** Your first FastAPI program
5. **Try:** Modifications from `main_template.py`

### For Experienced Developers:

1. **Scan:** `Quick_Command_Reference.md` 
2. **Copy:** `main_template.py`
3. **Run:** Commands and test
4. **Modify:** As needed

---

## ⚡ Quick Start (3 Steps)

```bash
# Step 1: Go to your Desktop and create a folder
cd Desktop
mkdir fastapi_learn
cd fastapi_learn

# Step 2: Create virtual environment and install FastAPI
python -m venv venv
.\venv\Scripts\activate  # Windows
# OR: source venv/bin/activate  # Mac/Linux
pip install fastapi uvicorn

# Step 3: Create main.py and copy code from main_template.py
# Then run:
uvicorn main:app --reload

# Open browser:
# http://localhost:8000/
```

---

## 📚 What You Will Learn

After following these guides, you will be able to:

✅ Install Python packages using pip  
✅ Create and activate a virtual environment  
✅ Build a basic FastAPI application  
✅ Run a local development server  
✅ Access your API in a web browser  
✅ Understand basic API concepts  
✅ Modify and create simple endpoints  
✅ Use the interactive API documentation  

---

## 🎓 Skill Levels

### Complete Beginner (Never coded before)
Start with: **FastAPI_Beginners_Setup_Guide.md**
- Read every section carefully
- Follow each step exactly
- Read the explanations

### Know Python but new to FastAPI
Start with: **Quick_Command_Reference.md**
- Use as a checklist
- Copy code from `main_template.py`
- Modify as needed

### Experienced Developer
Start with: **main_template.py**
- Copy the template
- Run it
- Modify to learn

---

## 💡 Tips

1. **Read error messages carefully** - They tell you what's wrong
2. **Check if virtual environment is active** - You should see `(venv)` in your terminal
3. **Use `--reload` flag** - It saves time during development
4. **Make sure `main.py` is in the right folder** - Same folder as `venv`
5. **Try modifications slowly** - Change one thing at a time
6. **Use `/docs` page** - The best way to test your API

---

## ⚠️ Common Issues

### Issue: "I don't see (venv) in my terminal"
**Solution:** Your virtual environment is not active. Activate it:
```bash
.\venv\Scripts\activate
```

### Issue: "Port 8000 already in use"
**Solution:** Use a different port:
```bash
uvicorn main:app --port 8001 --reload
```

### Issue: "Python not found"
**Solution:** Reinstall Python from [python.org](https://www.python.org)
Remember to check "Add Python to PATH"

### Issue: "FastAPI module not found"
**Solution:** Install it:
```bash
pip install fastapi uvicorn
```

**See `FastAPI_Beginners_Setup_Guide.md` for more solutions**

---

## 📖 Next Steps After Setup

Once you have your "Hello World" working:

1. **Try the modifications** in `main_template.py`
2. **Read the course notes** in `Class_2_Week_2_FastAPI_Basics.md`
3. **Run the examples** in `FastAPI_Starter_Examples/`
4. **Learn about:**
   - Path parameters (`/user/{id}`)
   - Query parameters (`/search?q=python`)
   - POST requests (sending data)
   - Data validation with Pydantic

---

## 🌍 Browser URLs to Try

When your server is running, try these URLs:

```
http://localhost:8000/               → Your API
http://localhost:8000/docs           → Interactive documentation
http://localhost:8000/redoc          → Alternative documentation
```

---

## 📞 Need Help?

### If something doesn't work:

1. **Read the error message** - It usually tells you what's wrong
2. **Check the troubleshooting section** in `FastAPI_Beginners_Setup_Guide.md`
3. **Make sure:**
   - Python is installed (`python --version`)
   - Virtual environment is activated (`(venv)` shows)
   - FastAPI is installed (`pip list` should show fastapi)
   - `main.py` is in the right folder
   - No typos in the code

### Common Fixes:

```bash
# Make sure virtual environment is active
.\venv\Scripts\activate

# Reinstall packages
pip install --upgrade fastapi uvicorn

# Check installed packages
pip list
```

---

## ✅ Success Checklist

Before you start:
- [ ] Python is installed
- [ ] You know how to open a terminal
- [ ] You know how to edit files
- [ ] You have 15-20 minutes

After completing the guide:
- [ ] Virtual environment created
- [ ] FastAPI installed
- [ ] `main.py` created
- [ ] Server running
- [ ] Browser shows "Hello World!"
- [ ] `/docs` page works

If all boxes checked ✅, you are ready to learn more!

---

## 🚀 You Are Ready!

Congratulations on taking the first step to learn FastAPI!

**Start with:** `FastAPI_Beginners_Setup_Guide.md`

**Happy Coding! 🎉**

---

## 📄 File Details

| File | Size | Purpose | Read Time |
|------|------|---------|-----------|
| FastAPI_Beginners_Setup_Guide.md | ~8KB | Complete step-by-step guide | 15-20 min |
| Quick_Command_Reference.md | ~4KB | Quick reference with commands | 5-10 min |
| main_template.py | ~2KB | Ready-to-use code template | 2 min |
| README.md | This file | Overview and help | 5 min |

---

**Start your FastAPI journey today! 🌟**
