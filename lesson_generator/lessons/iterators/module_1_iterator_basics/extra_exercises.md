```markdown
# Extra Exercises - Module 1: Introduction to Iterators

## Challenge 1: Identify Iterables vs. Iterators
**Goal:** Determine which of the following are iterables and which are iterators: `list`, `dict`, `set`, `map`, `filter`, `iter()`.  
**Hints:**  
- Recall that iterables can be looped over directly, while iterators require a call to `next()`.  
- Use the `isinstance()` function for checking types.

## Challenge 2: Create a Simple Iterable
**Goal:** Write a class named `MyRange` that behaves like Python's built-in `range()` and is iterable.  
**Hints:**  
- Implement `__iter__()` and `__next__()` methods.  
- Ensure it supports starting, stopping, and step values.

## Challenge 3: Implement the Iterator Protocol
**Goal:** Modify the `MyRange` class to include bounds checking and raise `StopIteration` appropriately.  
**Hints:**  
- Use an internal counter to track the current value.  
- Raise `StopIteration` when the counter exceeds the specified end value.

## Challenge 4: Create a Reverse Iterator
**Goal:** Develop a class called `Reverse` that takes a sequence and returns its elements in reverse order using the iterator protocol.  
**Hints:**  
- Use the `len()` function to get the size of the sequence.  
- Implement `__iter__()` to return `self` and `__next__()` to yield elements from the end of the sequence.

## Challenge 5: Custom Iterator with Filtering
**Goal:** Create a class `EvenIterator` that yields only even numbers from a given iterable.  
**Hints:**  
- Use the `__iter__()` and `__next__()` methods.  
- Check if numbers are even using modulus operator `%`.

## Challenge 6: Chaining Iterators
**Goal:** Write a function `chain_iterators(*iterables)` that takes multiple iterables and returns a single iterator that yields elements from each iterable in order.  
**Hints:**  
- Use a loop to iterate over each input iterable.  
- Utilize the `yield` keyword to create a generator.

## Challenge 7: Implement a Custom Iterable with Context
**Goal:** Create a class `FileLines` that reads a file and provides an iterator over its lines.  
**Hints:**  
- Implement `__iter__()` to open the file and `__next__()` to read lines.  
- Ensure the file is properly closed after iteration.

## Stretch Idea: Combine Iterators
**Goal:** Create a function `zip_iterators(*iterators)` that combines multiple iterators into a single iterator that yields tuples of elements.  
**Hints:**  
- Use the `next()` function on each iterator within a loop.  
- Handle `StopIteration` to break the loop when any iterator is exhausted.
```