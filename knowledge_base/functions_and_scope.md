# Python Functions and Scope

## 1. What is a Python Function?
A function in Python is an organized, reusable block of code designed to perform a specific action or calculation. Functions help break complex problems into manageable sub-tasks, foster code reuse, and adhere to the DRY (Don't Repeat Yourself) principle.

### Key Syntax:
```python
def function_name(parameters):
    """Optional docstring describing purpose."""
    # body of function
    return result
```

---

## 2. Basic Function Definition and Calling

### Example 1: Simple Greeting Function
```python
def greet(name):
    greeting = f"Hello, {name}!"
    return greeting

message = greet("Alice")
print(message)
```

### Step-by-Step Execution:
- **Definition**: Python registers function `greet` in symbol table.
- **Call**: `greet("Alice")` binds argument `"Alice"` to parameter `name`.
- **Local computation**: `greeting` is created with value `"Hello, Alice!"`.
- **Return**: The string is handed back to caller and stored into `message`.
- **Output**: `print(message)` displays `Hello, Alice!`.

---

## 3. Function Parameters and Arguments

Python supports multiple argument passing mechanisms:
1. **Positional Arguments**: Assigned based on the order they appear.
2. **Keyword Arguments**: Assigned explicitly by parameter name (`greet(name="Bob")`).
3. **Default Arguments**: Parameters with fallback values if omitted by caller.
4. **Arbitrary Positional Arguments (`*args`)**: Accepts variable count of arguments as tuple.
5. **Arbitrary Keyword Arguments (`**kwargs`)**: Accepts variable keyword arguments as dictionary.

### Example 2: Default Arguments & Calculations
```python
def calculate_price(unit_price, quantity=1, discount_rate=0.05):
    subtotal = unit_price * quantity
    discount = subtotal * discount_rate
    final_price = subtotal - discount
    return round(final_price, 2)

order1 = calculate_price(100.0)
order2 = calculate_price(100.0, 3, 0.10)
print(f"Order 1 Total: ${order1}")
print(f"Order 2 Total: ${order2}")
```

### Expected Output:
```text
Order 1 Total: $95.0
Order 2 Total: $270.0
```

---

## 4. Variable Scope: The LEGB Rule
In Python, variables are resolved according to the **LEGB rule**:
- **L**ocal: Names assigned within a function (not declared `global`).
- **E**nclosing: Names in the local scope of any enclosing functions (closures).
- **G**lobal: Names assigned at the top level of a module.
- **B**uilt-in: Names preassigned in the Python `builtins` module (`len`, `range`, `print`).

### Example 3: Demonstrating Scope
```python
x = 10  # Global variable

def modify_value():
    x = 20  # Local variable shadowing global x
    print("Inside function x =", x)

modify_value()
print("Outside function x =", x)
```

### Expected Output:
```text
Inside function x = 20
Outside function x = 10
```

---

## 5. Lambda Functions (Anonymous Functions)
A lambda function is a small anonymous function defined using the `lambda` keyword:
`lambda arguments: expression`

```python
square = lambda n: n ** 2
print(square(5))  # Output: 25
```
