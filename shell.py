from src.main import dixlang

while True:
    text = input('DixShell > ')
    
    if text.strip() == "": continue
    
    if text.strip() == 'exit': 
        break
    
    result, error = dixlang.run('<stdin>', text)

    if error:
        print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            print(repr(result.elements[0]))
        else:
            print(repr(result))