# DixLang 🚀

Welcome to **DixLang** – my very own programming language built from **SCRATCH** using Python!  
Whether you’re new to programming or a seasoned coder, DixLang offers a fun and approachable way to learn programming. Plus, it’s packed with features to help you get creative 😎!

---

## 📚 Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Language Syntax Overview](#language-syntax-overview)
    - [Comments](#comments)
    - [Variables & Arithmetic](#variables--arithmetic)
    - [Control Flow](#control-flow)
    - [Functions & Recursion](#functions--recursion)
    - [Lists & Strings](#lists--strings)
4. [Built-In Functions](#built-in-functions)
5. [Tutorials & Examples](#tutorials--examples)
6. [Advanced Topics](#advanced-topics)
7. [Running Scripts and REPL](#running-scripts-and-repl)
8. [Summary & Next Steps](#summary--next-steps)

---

## 1. Introduction
DixLang is an interpreted, BASIC-inspired language that is:
- **Simple:** Perfect for learning basic language concepts.
- **Expressive:** Supports arithmetic, control flow, recursive functions, and more!
- **Modular:** Easily extendable with built-in functions and custom syntax.

Learn by doing—experiment with code, explore the source, and have fun! 🤩

---

## 2. Getting Started
To start using DixLang:

1. **Clone the Repository:**  
   ```bash
   git clone https://github.com/sedfarouk/DixLang.git
   cd DixLang
   ```

2. **Run the REPL:**  
   Launch the interactive shell:
   ```bash
   python shell.py
   ```
   Then, try simple commands like:
   ```dxl
   5 + 3
   VAR x = 10
   WRITE(x)
   ```

3. **Execute a Script:**  
   Create a `.dxl` file (see the Tutorials section) and run it:
   ```dxl
   RUN("your_script.dxl")
   ```

4. **Exit:**  
   Simply type `exit` in the REPL.

---

## 3. Language Syntax Overview

### Comments  
Comments begin with a tilde `~`:
```dxl
~ This is a comment! 💬
```

### Variables & Arithmetic  
- **Declare Variables:** Use `VAR`
- **Operations:** `+`, `-`, `*`, `/`, `^`

Example:
```dxl
VAR a = 20
VAR b = 5

~ prints 25
WRITE(a + b)   
```

You can even do inline expressions:
```dxl
~ returns 4 and assigns 2 to x!
2 + (VAR x = 2)
```

### Control Flow

#### If / Eif / Else  
*Single-line:*
```dxl
IF a < 0 THEN WRITE("Negative!") EIF a == 0 THEN WRITE("Zero!") ELSE WRITE("Positive!")
```

*Multi-line:*
```dxl
IF a < 0 THEN
  WRITE("Negative!")
EIF a == 0 THEN
  WRITE("Zero!")
ELSE
  WRITE("Positive!")
END
```

#### Loops

**For Loop:**
```dxl
FOR i = 0 TO 5 THEN
    WRITE(i)
END
```

_Custom step:_
```dxl
FOR i = 10 TO 0 STEP -2 THEN
    WRITE(i)
END
```

**While Loop:**
```dxl
VAR count = 5
WHILE count > 0 THEN
    WRITE("Countdown: " + count)
    VAR count = count - 1
END
```

Loop controls (using `CONT` for continue and `BR` for break):
```dxl
FOR i = 1 TO 10 THEN
    IF i == 5 THEN
        WRITE("Found 5, stopping loop! ✋")
        BR
    END
    WRITE(i)
END
```

### Functions & Recursion  
Define functions with `FN`. They can be single-liners or multi-line blocks:

*One-liner:*
```dxl
FN greet(name) -> "Hello, " + name
WRITE(greet("Alice"))
```

*Recursive:*
```dxl
FN fib(n)
    IF n <= 1 THEN RET n
    RET fib(n - 1) + fib(n - 2)
END
WRITE("Fibonacci of 10 is: " + fib(10))
```

*Notes:*  
- `RET` allows for early returns.
- Functions are first-class citizens.

### Lists & Strings  
DixLang allows you to work with arrays and strings naturally.

**Lists:**
```dxl
VAR numbers = [1, 2, 3, 4]

~ prints [1, 2, 3, 4]
WRITE(numbers)   

APPEND(numbers, 5)

~ prints [1, 2, 3, 4, 5]
WRITE(numbers)   
```

**Strings:**
```dxl
VAR greeting = "Hello, " + "World!"
WRITE(greeting)
```

---

## 4. Built-In Functions

DixLang includes a helpful set of built-in functions:

| **Function**         | **Description**                                  | **Example**                    |
| -------------------- | ------------------------------------------------ | ------------------------------ |
| `WRITE(value)`       | Prints output to the console                   | `WRITE("Hello!")`              |
| `WRITE_RET(value)`   | Prints and returns the value as a string         | `WRITE_RET("Echo!")`           |
| `INPUT()`            | Reads a line of user input                       | `VAR name = INPUT()`           |
| `INPUT_INT()`        | Reads an integer                                 | `VAR num = INPUT_INT()`        |
| `CLEAR()`            | Clears the terminal screen                       | `CLEAR()`                      |
| `IS_NUM(value)`      | Checks if the value is a number                  | `IS_NUM(42)`                   |
| `IS_STR(value)`      | Checks if the value is a string                  | `IS_STR("foo")`                |
| `IS_LIST(value)`     | Checks if the value is a list                    | `IS_LIST([1,2,3])`             |
| `IS_FN(value)`       | Checks if the value is a function                | `IS_FN(greet)`                 |
| `APPEND(list, value)`| Appends an element to a list                     | `APPEND(numbers, 10)`          |
| `POP(list, index)`   | Removes and returns an element at a specific index | `POP(numbers, 1)`              |
| `EXTEND(listA, listB)`| Merges two lists                                | `EXTEND(list1, list2)`         |
| `LENGTH(list)`       | Returns the length of a list                     | `LENGTH(numbers)`              |
| `RUN(fn)`            | Executes another DixLang script                  | `RUN("script.dxl")`            |
| `RANDOM_INT(lo, hi)` | Returns a random integer between lo and hi       | `RANDOM_INT(1, 10)`            |

---

## 5. Tutorials & Examples

### Tutorial 1: Basic Arithmetic and Variables
- **Step 1:** Open the REPL.
- **Step 2:** Type:
  ```dxl
  VAR x = 7
  VAR y = 3

  ~ Should print 10
  WRITE(x + y)  
  ```
- **Step 3:** Experiment with inline declarations:
  ```dxl
  ~ returns 11
  WRITE((VAR a = 5) + (VAR b = 2) * 3) 
  ```

---

### Tutorial 2: Control Flow Demonstration
Try conditional statements:
```dxl
VAR number = 4
IF number < 0 THEN
    WRITE("Negative!")
ELIF number == 0 THEN
    WRITE("Zero!")
ELSE
    WRITE("Positive!")
END
```

Then test a loop:
```dxl
FOR i = 1 TO 5 THEN
    IF i == 3 THEN
        WRITE("Skipping 3! ✌️")
        CONT
    END
    WRITE(i)
END
```

---

### Tutorial 3: Creating and Using Functions
Start with a simple arithmetic function:
```dxl
FN add(a, b) -> a + b
WRITE("Sum is: " + add(10, 15))
```

Now, try a recursive Fibonacci function:
```dxl
FN fib(n)
    IF n <= 1 THEN RET n
    RET fib(n - 1) + fib(n - 2)
END
WRITE("Fib(7): " + fib(7))
```

---

### Tutorial 4: Lists, Strings, and Built-Ins
Work with lists:
```dxl
VAR myList = [1, 2, 3]
APPEND(myList, 4)

~ Expect: [1, 2, 3, 4]
WRITE(myList)     
WRITE("Length: " + LENGTH(myList))
```

And strings:
```dxl
FN exclaim(s) -> s + "!"
WRITE(exclaim("Hello"))
```

---

### Example Script: test_file_exec.dxl
Here's a sample script combining multiple features:
```dxl
// file: test_file_exec.dxl
WRITE("I FINALLY DID IT! MY OWN PROGRAMMING LANGUAGE! 😎")

~ Function to concatenate strings
FN concatenate(prefix, suffix) -> prefix + suffix

FOR i = 0 TO 5 THEN
    WRITE(concatenate("Iteration ", i))
END

FN fib(n)
    IF n <= 1 THEN RET n
    RET fib(n - 1) + fib(n - 2)
END

WRITE("Fibonacci of 10: " + fib(10))
```
_Run it by typing:_
```dxl
RUN("c:\\Users\\FaroukS\\Desktop\\DixLang\\test_file_exec.dxl")
```

---

## 6. Advanced Topics <details>
<summary>Click to Expand Advanced Topics 🔍</summary>

### Error Reporting and Debugging
DixLang reports errors with clear messages and visual arrows:
```
Invalid Syntax: Expected '+', '-', '*', '^' or '/'
File test_file_exec.dxl, line 10
       ^^^
```
This helps you pinpoint the exact location and nature of issues.

### Interpreter Internals
Learn how DixLang works under the hood:
- **Lexing:** Converts source code into tokens.
- **Parsing:** Builds an Abstract Syntax Tree (AST) from tokens.
- **Evaluation:** The interpreter processes the AST to produce results.

### Custom Extensions
Developers can extend the language by adding new built-in functions or syntax rules. Explore files in `src/values/functions/` and `src/constants/` for ideas.

</details>

---

## 7. Future Enhancements
The future roadmap for DixLang includes a variety of exciting improvements and new features:

- **Improved Error Messages:**  
  Enhance error reporting with more detailed suggestions and context-aware hints.

- **Debugging Tools:**  
  Develop built-in debugging commands to step through code and inspect variables at runtime.

- **Extended Library:**  
  Add more built-in functions, including file I/O operations, networking, and graphics modules.

- **Enhanced Syntax:**  
  Introduce additional syntactic sugar such as switch-case constructs and list comprehensions.

- **Module System:**  
  Implement an import system for better code reusability and module management.

- **Performance Optimizations:**  
  Refine the interpreter to improve execution speed and memory management.

- **Community Contributions:**  
  Encourage community-driven extensions, tutorials, and educational resources.

Stay tuned for updates and feel free to propose new ideas!

---

## 8. Running Scripts and REPL
- **Interactive REPL:** Run:
  ```bash
  python shell.py
  ```
  Then, try commands like:
  ```dxl
  VAR a = 100

  ~ prints 50
  WRITE(a / 2)   
  ```

- **Batch Scripts:** Save your code as a `.dxl` file and execute it:
  ```dxl
  RUN("c:\\Users\\FaroukS\\Desktop\\DixLang\\your_script.dxl")
  ```

---

## 9. Summary & Next Steps
DixLang is a versatile playground:
- **Arithmetic & Variables:** Start with simple maths.
- **Control Flow:** Use conditionals and loops.
- **Functions:** Define, call, and even recurse.
- **Lists & Strings:** Manipulate collections and text.
- **Built-Ins:** Leverage I/O and utility functions.

Feel free to explore, modify, and extend the language by diving into the `src/` folder. Happy coding and enjoy your journey with DixLang! 🎉

---

*For issues, suggestions, or contributions, please head over to the GitHub repository and open an issue or pull request. With love, Farouk ❤️*