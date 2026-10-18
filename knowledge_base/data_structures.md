# Python Built-In Data Structures

## 1. Overview
Python provides four foundational built-in data structures:
- **List**: Ordered, mutable, allows duplicate members. Defined with `[]`.
- **Tuple**: Ordered, immutable, allows duplicate members. Defined with `()`.
- **Set**: Unordered, mutable, unique elements only. Defined with `{}`.
- **Dictionary**: Key-value pairs, ordered (since Python 3.7), mutable, unique keys. Defined with `{key: value}`.

---

## 2. Lists and List Comprehensions

### Core Operations
```python
fruits = ["apple", "banana", "cherry"]
fruits.append("mango")       # Adds to end
fruits.insert(1, "orange")   # Inserts at index 1
removed_item = fruits.pop()  # Removes and returns last element
print("List:", fruits)
```

### List Comprehension
List comprehensions provide a concise way to create lists based on existing iterables:
`[expression for item in iterable if condition]`

### Example 1: Even Squares
```python
numbers = [1, 2, 3, 4, 5, 6]
even_squares = [x**2 for x in numbers if x % 2 == 0]
print("Even Squares:", even_squares)
```
**Output:** `Even Squares: [4, 16, 36]`

---

## 3. Dictionaries (Key-Value Mappings)

### Example 2: Managing Student Records
```python
student = {
    "id": "STU101",
    "name": "Ananya",
    "course": "Computer Science",
    "grades": [92, 88, 95]
}

# Accessing and modifying
student["semester"] = 4
average_grade = sum(student["grades"]) / len(student["grades"])

print(f"Student: {student['name']}")
print(f"Average Grade: {average_grade:.2f}")

# Iterating keys and values
for key, value in student.items():
    print(f" - {key}: {value}")
```

### Step-by-Step Breakdown:
1. Creates dictionary with keys `id`, `name`, `course`, `grades`.
2. Adds key `semester` with integer `4`.
3. Computes average from numeric list `[92, 88, 95]`.
4. Loops through `student.items()` yielding `(key, value)` tuples.

---

## 4. Sets and Tuples

### Sets (Mathematical Set Operations)
```python
set_a = {1, 2, 3, 4}
set_b = {3, 4, 5, 6}

union_set = set_a | set_b        # {1, 2, 3, 4, 5, 6}
intersection = set_a & set_b     # {3, 4}
difference = set_a - set_b       # {1, 2}
```

### Tuples (Immutable Records)
```python
point = (10, 20)
x, y = point  # Tuple unpacking
print(f"X: {x}, Y: {y}")
```
