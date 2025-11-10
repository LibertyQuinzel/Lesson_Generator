```markdown
# Extra Exercises - Module 2: Creating Custom Iterators

## Challenge 1: Basic Custom Iterator
**Goal:** Create a custom iterator class that yields numbers from 1 to 10.  
**Hints:**  
- Define a class with `__iter__()` and `__next__()` methods.  
- Use an instance variable to track the current number.  

## Challenge 2: Reverse String Iterator
**Goal:** Implement an iterator that takes a string and yields its characters in reverse order.  
**Hints:**  
- Utilize `__iter__()` and `__next__()` methods.  
- Consider using an index that starts at the end of the string.  

## Challenge 3: Fibonacci Generator Function
**Goal:** Write a generator function that yields Fibonacci numbers up to a specified limit.  
**Hints:**  
- Use a `while` loop to generate numbers.  
- Maintain two variables to track the last two Fibonacci numbers.  

## Challenge 4: Custom Range Iterator
**Goal:** Create a custom iterator that mimics Python's built-in `range()` function.  
**Hints:**  
- Accept start, stop, and step parameters in your iterator class.  
- Handle cases where start is greater than stop.  

## Challenge 5: Prime Number Generator
**Goal:** Write a generator function that yields prime numbers indefinitely.  
**Hints:**  
- Use a helper function to check for primality.  
- Keep track of the current number and increment it in each iteration.  

## Challenge 6: Chained Iterators
**Goal:** Build a class that combines multiple iterators into a single iterator.  
**Hints:**  
- Store the iterators in a list.  
- In `__next__()`, iterate through each iterator until one is exhausted.  

## Challenge 7: File Line Iterator
**Goal:** Create an iterator that reads lines from a file and yields them one by one.  
**Hints:**  
- Open the file in `__iter__()` and close it in `__next__()`.  
- Handle `StopIteration` when reaching the end of the file.  

## Challenge 8: Stretch - Infinite Geometric Sequence Generator
**Goal:** Implement a generator that yields terms of a geometric sequence indefinitely.  
**Hints:**  
- Accept initial term and common ratio as parameters.  
- Use a loop to continuously yield the next term by multiplying the previous term.  
- Consider how to gracefully handle very large numbers.
```
