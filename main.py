import re
from rich import print

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
        return {"expression": expression, "error": error_index}
    
    # Check if the expression ends with an operator
    if expression[-1] in '+-*/':
        return {"expression": expression, "error": len(expression) - 1}
    
    # Check if the first character is an operator other than + or -
    if expression[0] in '*/':
        return {"expression": expression, "error": 0}
    
    # Check for consecutive operators within the expression
    for i in range(1, len(expression) - 1):
        if expression[i] in '+-*/' and expression[i+1] in '+-*/':
            return {"expression": expression, "error": i}
    
    return {"expression": expression, "error": None}
    
    



def main():

    print("[bold blue]\n******Welcome to Dipalo******\n[/bold blue]")

    expression = ''

    while expression.lower() != "exit":
        expression = input("Enter your expression: \n")

        # clean expression
        expression = clean_expression(expression)

        if expression["error"] is not None:
            print("Illegal character found at index:", expression["error"])
    

if "__main__" == __name__:

    main()