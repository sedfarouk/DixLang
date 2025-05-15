# DixLang 🚀

Welcome to **DixLang** – your very own programming language built from scratch using Python!  
Whether you’re new to programming or a seasoned coder, DixLang offers a fun, approachable way to learn about language design, lexing/parsing, and basic interpreter internals.  
Plus, it comes loaded with features to help you get creative 😎!

---

## Table of Contents
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

## Introduction
DixLang is an interpreted language inspired by BASIC – simple yet powerful enough for arithmetic, control flow, and even recursive functions!  
It was built to experiment with language concepts like lexing, parsing, and AST evaluation.  
Here you’ll find tutorials along with creative examples so you can explore programming in a new way. 🤩

---

## Getting Started
To begin using DixLang:
1. **Clone the Repository:**  
   Open your terminal and run:  
   ```bash
   git clone https://your.repo.url/DixLang.git
   cd DixLang
   ```

2. **Run the REPL:**  
   Launch the interactive shell with:  
   ```bash
   python -m src.main.dixlang
   ```
   Then, try out simple expressions like `5 + 3` or variable assignments.

3. **Execute a Script:**  
   Create a `.dxl` file (see [Tutorials & Examples](#tutorials--examples)) and run it from the REPL using:  
   ```dxl
   RUN("your_script.dxl")
   ```

---

## Language Syntax Overview

### Comments  
Write simple comments using the tilde (`~`):  
```dxl
~ This is a comment! 💬
```

### Variables & Arithmetic  
- **Variable Declaration:** Use `VAR` to declare variables.
- **Arithmetic Operations:** Supports `+`, `-`, `*`, `/`, and `^`.

Example:
```dxl
VAR a = 20
VAR b = 5
WRITE(a + b)   ~ prints 25
```

For inline expressions:
```dxl
2 + (VAR x = 2)   ~ returns 4 and assigns 2 to x!
```

### Control Flow
Control statements make your code dynamic!
  
#### If/Eif/Else  
Single-line and multi-line if expressions are supported.

*Single-line example:*
```dxl
IF a < 0 THEN WRITE("Negative!") EIF a == 0 THEN WRITE("Zero!") ELSE WRITE("Positive!") END
```

*Multi-line example:*
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
**For Loop**  
Iterate using `FOR` with an optional step.

Example:
```dxl
FOR i = 0 TO 5 THEN
    WRITE(i)
END
```

Custom step:
```dxl
FOR i = 10 TO 0 STEP -2 THEN
    WRITE(i)
END
```

**While Loop**  
Keep looping until the condition changes:
```dxl
VAR count = 5
WHILE count > 0 THEN
    WRITE("Countdown: " + count)
    VAR count = count - 1
END
```

Loop controls such as `CONT` (continue) and `BR` (break) let you manage iterations:
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
Define functions with `FN`. Functions can be one-liners or use a block for multiple statements and even recursion!

*One-liner function:*
```dxl
FN greet(name) -> "Hello, " + name
WRITE(greet("Alice"))
```

*Recursive function:*
```dxl
FN fib(n)
    IF n <= 1 THEN RET n
    RET fib(n - 1) + fib(n - 2)
END

WRITE("Fibonacci of 10 is: " + fib(10))
```

*Note:*  
- `RET` is used for early return inside functions.
- Functions are first-class citizens; you can even assign them to variables!

### Lists & Strings  
DixLang supports basic list and string operations.

**Lists:**
```dxl
VAR numbers = [1, 2, 3, 4]
WRITE(numbers)   ~ prints [1, 2, 3, 4]
```

You can even perform operations like appending elements:
```dxl
APPEND(numbers, 5)
WRITE(numbers)
```

**Strings:**
```dxl
VAR greeting = "Hello, " + "World!"
WRITE(greeting)
```

---

## Built-In Functions
DixLang comes with a set of built-in functions to handle I/O and list operations:

| Function         | Description                                                            | Example Usage                                     |
| ---------------- | ---------------------------------------------------------------------- | ------------------------------------------------- |
| `WRITE(value)`   | Prints output to the console                                           | `WRITE("Hello!")`                                 |
| `WRITE_RET(value)` | Prints and returns the value as a string                              | `WRITE_RET("Echo!")`                              |
| `INPUT()`        | Reads input from the user                                              | `VAR name = INPUT()`                              |
| `INPUT_INT()`    | Reads an integer                                                     | `VAR num = INPUT_INT()`                           |
| `CLEAR()`        | Clears the terminal screen                                             | `CLEAR()`                                         |
| `IS_NUM(value)`  | Returns true if value is a number                                      | `IS_NUM(42)`                                      |
| `IS_STR(value)`  | Returns true if value is a string                                      | `IS_STR("foo")`                                   |
| `IS_LIST(value)` | Checks if value is a list                                              | `IS_LIST([1,2,3])`                                |
| `IS_FN(value)`   | Checks if value is a function                                          | `IS_FN(greet)`                                    |
| `APPEND(list, value)` | Appends an element to a list                                         | `APPEND(numbers, 10)`                             |
| `POP(list, index)`  | Removes and returns an element from a list at the specified index     | `POP(numbers, 1)`                                 |
| `EXTEND(listA, listB)` | Merges two lists into one                                              | `EXTEND(list1, list2)`                            |
| `LENGTH(list)`   | Returns the length of a list                                           | `LENGTH(numbers)`                                 |
| `RUN(fn)`        | Executes another DixLang script                                        | `RUN("script.dxl")`                               |

---

## Tutorials & Examples

### Tutorial 1: Basic Arithmetic and Variables
1. Open your REPL and type:
   ```dxl
   VAR x = 7
   VAR y = 3
   WRITE(x + y)  ~ Should print 10
   ```
2. Experiment by changing values and combining operations:
   ```dxl
   WRITE((VAR a = 5) + (VAR b = 2) * 3)   ~ returns 11
   ```

### Tutorial 2: Control Flow Demonstration
Learn about conditionals and loops:
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

Then, try a loop:
```dxl
FOR i = 1 TO 5 THEN
    IF i == 3 THEN
        WRITE("Skipping 3! ✌️")
        CONT
    END
    WRITE(i)
END
```

### Tutorial 3: Creating and Using Functions
Start with a simple function:
```dxl
FN add(a, b) -> a + b
WRITE("Sum is: " + add(10, 15))
```

Now, create a recursive function (Fibonacci):
```dxl
FN fib(n)
    IF n <= 1 THEN RET n
    RET fib(n - 1) + fib(n - 2)
END
WRITE("Fib(7): " + fib(7))
```

### Tutorial 4: Lists, Strings, and Built-Ins
Work with lists and use built-in functions:
```dxl
VAR myList = [1, 2, 3]
APPEND(myList, 4)
WRITE(myList)   ~ Expect: [1, 2, 3, 4]
WRITE("Length: " + LENGTH(myList))
```

Use string functions:
```dxl
FN exclaim(s) -> s + "!"
WRITE(exclaim("Hello"))
```

### Example Script: test_file_exec.dxl
Below is a sample DixLang script that shows multiple features in one file:
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
Run it by issuing in the REPL:
```dxl
RUN("c:\\Users\\FaroukS\\Desktop\\DixLang\\test_file_exec.dxl")
```

---

## Advanced Topics <details>
<summary>Click to Expand Advanced Topics 🔍</summary>

### Error Reporting and Debugging
DixLang uses a robust error reporting system. When a syntax error occurs, you’ll see detailed messages along with an arrow pointing to the error location:
```
Invalid Syntax: Expected '+', '-', '*', '^' or '/'
File test_file_exec.dxl, line 10
       ^^^
```

### Interpreter Internals
- **Lexing:** Converts raw text into tokens (e.g., numbers, operators, identifiers).
- **Parsing:** Builds the Abstract Syntax Tree (AST) from tokens.
- **Evaluation:** The Interpreter walks the AST and computes the result.

### Custom Extensions
Developers can extend DixLang by adding new built-in functions or additional syntax rules. Check out the source files in `src/values/functions/` and `src/constants/` for inspiration.

</details>

---

## Running Scripts and REPL
- **Interactive REPL:** Run `python -m src.main.dixlang` and type commands one at a time.  
  Example session:
  ```text
  DixShell > VAR a = 100
  DixShell > WRITE(a / 2)
  50
  ```
- **Batch Scripts:** Save your DixLang code in a file with the `.dxl` extension and run it using:
  ```dxl
  RUN("c:\\Users\\FaroukS\\Desktop\\DixLang\\your_script.dxl")
  ```

---

## Summary & Next Steps
DixLang is designed to be a playground for both learners and language enthusiasts. You now know how to:
- Write basic arithmetic and variable assignments.
- Use control flow and loops.
- Create functions, including recursive ones.
- Manipulate strings and lists.
- Leverage built-in functions for common tasks.

Feel free to modify the interpreter, add new syntactic features, or extend the language. Dive into the code under the `src/` folder to see how tokenization, parsing, and interpreting work!

Happy coding and have fun exploring DixLang! 🎉

---

*For any issues or contributions, please refer to our GitHub repository and open a discussion or pull request.*