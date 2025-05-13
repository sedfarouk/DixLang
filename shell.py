from src.main.dixlang import run

while True:
    text = input('DixShell > ')
    
    if text == 'exit': 
        break
    
    result, error = run('<stdin>', text)

    if error:
        print(error.as_string())
    elif result:
        print(repr(result))