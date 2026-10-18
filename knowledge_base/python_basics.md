# Python Fundamentals and Syntax Basics

## 1. Variables and Data Types
Python is dynamically typed. You don't need to declare data types explicitly.
Standard types:
- `int`: 42, -5
- `float`: 3.14159
- `str`: "Hello World"
- `bool`: True, False
- `NoneType`: None

```python
x = 10
pi = 3.14
greeting = "Welcome to Python Tutor"
is_active = True
```

---

## 2. Conditional Statements (`if`, `elif`, `else`)

```python
score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"
print(f"Grade: {grade}")
```

---

## 3. String Manipulation & F-Strings
Formatted string literals (f-strings) provide concise expression interpolation:
```python
name = "Alex"
score = 98.567
print(f"Student: {name.upper()}, Score: {score:.1f}%")
```
