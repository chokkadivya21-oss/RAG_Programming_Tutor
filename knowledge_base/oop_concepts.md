# Object-Oriented Programming (OOP) in Python

## 1. Core Principles of OOP
Object-Oriented Programming models real-world software components as objects that encapsulate data (attributes) and behavior (methods).

The 4 pillars of OOP are:
1. **Encapsulation**: Bundling data with methods that operate on that data and restricting direct access.
2. **Inheritance**: Creating new classes based on existing classes to reuse code.
3. **Polymorphism**: Ability for different classes to be treated through a common interface.
4. **Abstraction**: Hiding internal implementation details and exposing only the essential interface.

---

## 2. Classes and Objects in Python

### The `__init__` Constructor and `self`
- `__init__`: Special initializer method executed whenever a new instance is created.
- `self`: Reference pointing to the current instance of the class.

### Example 1: Bank Account Class
```python
class BankAccount:
    def __init__(self, account_holder, balance=0.0):
        self.account_holder = account_holder
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        return self.balance

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew ${amount}. Remaining balance: ${self.balance}")
            return True
        print("Insufficient funds or invalid amount!")
        return False

# Demonstration
acc = BankAccount("Sumanth", 100.0)
acc.deposit(50.0)
acc.withdraw(30.0)
```

---

## 3. Inheritance and Method Overriding

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Generic sound"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

animals = [Dog("Buddy"), Cat("Luna")]
for a in animals:
    print(a.speak())
```
