# Python Basics

## Variables

Variables give names to values:

```python
learner = "Alex"
completed_lessons = 3
print(f"{learner} has completed {completed_lessons} lessons.")
```

## Conditions

Use `if` and `else` to choose what a program does:

```python
temperature = 18

if temperature < 20:
    print("Bring a jacket.")
else:
    print("A light layer should be fine.")
```

## Loops

Use a `for` loop to repeat an action for each item:

```python
topics = ["strings", "lists", "functions"]

for topic in topics:
    print(f"Next topic: {topic}")
```

## Functions

Functions package a reusable task:

```python
def greet(name):
    return f"Hello, {name}!"


print(greet("Python learner"))
```
