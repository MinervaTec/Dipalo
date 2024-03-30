import re

def separate_expression(expression):
    # Using regular expression to split numbers and operators
    numbers = re.findall(r'[0-9.]+', expression)
    operators = re.findall(r'[+\-*/]', expression)
    
    return numbers, operators

def clean_expression(expression):
    # Check for illegal characters using regular expression
    illegal_chars = re.findall(r'[^0-9.+\-*/]', expression)
    
    if illegal_chars:
        error_index = expression.index(illegal_chars[0])
        return {"expr": expression, "error": error_index}
    
    # Check if the expression ends with an operator
    if expression[-1] in '+-*/':
        return {"expr": expression, "error": len(expression) - 1}
    
    # Check if the first character is an operator other than + or -
    # if expression[0] in '*/':
    #     return {"expr": expression, "error": 0}
    
    # Check for consecutive operators within the expression
    for i in range(1, len(expression) - 1):
        if expression[i] in '+-*/' and expression[i+1] in '+-*/':
            return {"expr": expression, "error": i}
    
    return {"expr": expression, "error": None}


def main():
    
    history = []

    print("[bold blue]\n******Welcome to Dipalo******\n[/bold blue]")

    crnt_expression = ''

    while True:

        crnt_expression = input("Enter your expression: \n")

        if crnt_expression.lower() == "exit":
            break

        # clean crnt_expression
        crnt_expression = clean_expression(crnt_expression)

        if crnt_expression["error"] is not None:
            print("Illegal character found at index:", crnt_expression["error"])
            continue

        # create a new history expression with unique id
        unique_id = check_unique_id(history)

        # make expression to be string again
        crnt_expression = crnt_expression["expr"]


        result = perform_operations(separate_expression(crnt_expression), [])

        history.append( {
            "id":unique_id,
            "expression":crnt_expression,
            "steps":result[1],
            "result":result[0]
        })
    
        print("-------------")
        print(result[0])
        print(result[1])
        print("\n")

if "__main__" == __name__:

    main()