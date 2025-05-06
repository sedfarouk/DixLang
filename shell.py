from dixlang import run

while True:
    text = input('DixShell > ')
    result, error = run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)