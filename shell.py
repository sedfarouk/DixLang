from basic import run

while True:
    text = input('BasicxShell > ')
    result, error = run('<stdin>', text)

    if error:
        print(error.as_string())
    else:
        print(result)