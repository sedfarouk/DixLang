# DixLang
Yesss, you read that right! Dix...Lang. I have always wanted to do this - create my own language from **SCRATCH** and at least put my DSA skills to good use...brr 😎 - but felt lazyyyy...

Out of no particular reason, I have started and chose to build an interpreted language using Python. DixLang is inspired by BASIC (cos it's a simple language, lol). Might think of building a compiled language after this but building this can at least satisfy my desire to learn more about how programming languages work 💪!

...and yes, I know it's gonna be buried in the cemetries of Git 💀 but I don't plan on being the next Dennis Ritchie 😅

## Current Progress

- **Arithmetic Operations:**  
  - Perform binary (addition, subtraction, multiplication, division, exponentiation) and unary (negation) operations.

- **Lexing & Parsing:**  
  - Tokenization of input for numbers, arithmetic operators, parentheses, and variable keywords.
  - Parsing of tokens into an abstract syntax tree (AST).

- **Interpreting:**  
  - Evaluation of the AST to calculate arithmetic expressions.
  - Error detection and location reporting for syntax errors.

- **Variables:**  
    - You can now assign variables using the `VAR` keyword (e.g., `VAR a = 20`).
    - Variables can be used anywhere in expressions.
    - You can even assign a variable as part of an expression, for example: `2 + (VAR x = 2)` will return 4 while storing the value `2` in variable `x`.

## What You Can Currently Do

- Run arithmetic expressions through the interactive console, for example:
  - `5 + 3`
  - `-2 * (4 + 1)`
  - `2 ^ 2`
  - `VAR a = 20`
  - `2 + (VAR x = 2)`  *(returns 4 with `x` storing the value `2`)*

- View immediate results of calculations and detailed error messages on faulty expressions.

## Snapshots

Snapshots of the program in action will be included below to demonstrate:
- The interactive shell processing valid arithmetic expressions and variable assignments.
- The error output when syntax errors are detected.

![Arithmetic Operations](screenshots/arithmetic_op.png)

![Syntax Error](screenshots/arithmetic_invalid_syntax.png)

![Variables](screenshots/int_var.png)