# Python Loops and Iteration

## 1. Introduction to Loops
Loops in Python are control flow statements used to repeatedly execute a block of code as long as a specified condition is satisfied or for each element in an iterable sequence.
Python primarily provides two loop constructs:
1. `for` loop: Definite iteration over an iterable (range, list, tuple, string, dictionary).
2. `while` loop: Indefinite iteration based on a boolean condition.

---

## 2. The `for` Loop with `range()`

### Concept
The `for` loop iterates over items of any sequence in order. When combined with the built-in `range(start, stop, step)` function, it generates an arithmetic progression of integers starting at `start` and ending at `stop - 1`.

### Example 1: Basic Counting Loop
```python
for i in range(1, 4):
    print(i)
```

### Step-by-Step Execution:
- **Initialization**: `range(1, 4)` produces sequence `[1, 2, 3]`.
- **Iteration 1**: `i` is assigned `1`. Body executes `print(1)`. Output: `1`.
- **Iteration 2**: `i` is assigned `2`. Body executes `print(2)`. Output: `2`.
- **Iteration 3**: `i` is assigned `3`. Body executes `print(3)`. Output: `3`.
- **Termination**: Sequence is exhausted. Loop terminates gracefully.

### Expected Output:
```text
1
2
3
```

---

## 3. Accumulator Pattern with Loops

### Concept
An accumulator is a variable used within a loop to keep a running total or combined result across iterations.

### Example 2: Calculating Sum of Numbers
```python
total = 0
for num in [10, 20, 30]:
    total = total + num
    print(f"Added {num}, running total: {total}")
print(f"Final Total: {total}")
```

### Expected Output:
```text
Added 10, running total: 10
Added 20, running total: 30
Added 30, running total: 60
Final Total: 60
```

---

## 4. The `while` Loop

### Concept
The `while` loop repeatedly executes as long as its test expression remains `True`. It requires careful management of loop counter variables to avoid infinite loops.

### Example 3: Countdown Loop
```python
count = 3
while count > 0:
    print("Countdown:", count)
    count -= 1
print("Blast off!")
```

### Step-by-Step Trace:
- Step 1: `count = 3`. Condition `3 > 0` is `True`. Prints `Countdown: 3`. Decrements `count` to `2`.
- Step 2: `count = 2`. Condition `2 > 0` is `True`. Prints `Countdown: 2`. Decrements `count` to `1`.
- Step 3: `count = 1`. Condition `1 > 0` is `True`. Prints `Countdown: 1`. Decrements `count` to `0`.
- Step 4: `count = 0`. Condition `0 > 0` is `False`. Loop exits. Prints `Blast off!`.

---

## 5. Loop Control Statements: `break`, `continue`, `pass`

- `break`: Terminates the nearest enclosing loop immediately.
- `continue`: Skips the rest of the current iteration and jumps to the next cycle.
- `pass`: Null operation / placeholder when a statement is syntactically required.

### Example 4: Using `break` and `continue`
```python
for n in range(1, 6):
    if n == 2:
        continue  # skip 2
    if n == 5:
        break     # stop at 5
    print(f"Number: {n}")
```

### Expected Output:
```text
Number: 1
Number: 3
Number: 4
```

---

## 6. Common Pitfalls & Best Practices
- **Off-by-one errors**: Remember that `range(1, 5)` generates `1, 2, 3, 4` (does NOT include `5`).
- **Infinite while loops**: Always ensure the variable inside the `while` condition changes state toward termination.
- **Modifying list while iterating**: Avoid removing or inserting items in a list while iterating over it; iterate over a copy `my_list[:]` instead.
