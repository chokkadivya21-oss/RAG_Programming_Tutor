# Python Exception Handling and Robust Code

## 1. Understanding Errors vs. Exceptions
- **Syntax Errors**: Errors in code grammar detected by the parser before running the program.
- **Exceptions**: Logical errors or unforeseen runtime conditions detected during program execution (e.g., `ZeroDivisionError`, `IndexError`, `KeyError`, `ValueError`).

---

## 2. The `try ... except ... else ... finally` Pattern

```python
try:
    # Code that might raise an exception
    num = int("123")
    result = 10 / num
except ValueError:
    print("Error: Invalid numeric format")
except ZeroDivisionError:
    print("Error: Cannot divide by zero")
else:
    # Runs ONLY if no exceptions were raised
    print(f"Success! Calculation result is {result}")
finally:
    # Runs ALWAYS, regardless of errors (useful for resource cleanup)
    print("Execution of error-handling block finished.")
```

---

## 3. Raising Custom Exceptions

```python
def validate_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")
    if age > 120:
        raise ValueError("Age is unrealistically high.")
    return True
```
