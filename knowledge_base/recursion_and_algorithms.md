# Recursion and Algorithmic Thinking in Python

## 1. What is Recursion?
Recursion is a programming technique where a function solves a problem by calling itself with smaller sub-problems.
Every recursive function requires two essential components:
1. **Base Case**: The condition under which the function stops calling itself and returns a result directly.
2. **Recursive Case**: The logic that reduces the problem size and invokes the function again.

Without a base case, recursion leads to a `RecursionError: maximum recursion depth exceeded`.

---

## 2. Factorial Example

### Concept:
\( n! = n \times (n-1)! \), with base case \( 0! = 1 \) and \( 1! = 1 \).

### Code:
```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

result = factorial(4)
print(f"4! = {result}")
```

### Call Stack Visualization:
1. `factorial(4)` calls `4 * factorial(3)`
2. `factorial(3)` calls `3 * factorial(2)`
3. `factorial(2)` calls `2 * factorial(1)`
4. `factorial(1)` hits base case, returns `1`
5. Unwinding: `2 * 1 = 2` -> `3 * 2 = 6` -> `4 * 6 = 24`.

---

## 3. Fibonacci Sequence

```python
def fibonacci(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

series = [fibonacci(i) for i in range(7)]
print("Fibonacci series:", series)
```
**Output:** `Fibonacci series: [0, 1, 1, 2, 3, 5, 8]`
