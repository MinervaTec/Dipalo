import re
from rich import print
import random
import string

def generate_id():
    # Generate a random ID
    id = ''.join(random.choices(string.digits + string.ascii_lowercase, k=4))
    return id

def check_unique_id(history):
    while True:
        new_id = generate_id()  # Generate a new ID
        if new_id not in [expr['id'] for expr in history]:
            return new_id  # Return the unique ID

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
    
    
def perform_operations(numbers, operators):
    # Define the priority of operators based on BODMAS/BIDMAS
    operator_priority = {'*': 2, '/': 2, '+': 1, '-': 1}

      # Handle operations within brackets recursively
    while '(' in operators:
        start_index = operators.index('(')
        end_index = start_index + operators[start_index:].index(')')
        
        # Perform operations within the brackets
        result_within_brackets = perform_operations(numbers[start_index:end_index],
                                                    operators[start_index + 1:end_index])
        
        # Update numbers and operators lists after evaluating brackets
        numbers[start_index] = result_within_brackets
        del numbers[start_index + 1:end_index + 1]
        del operators[start_index:end_index + 1]

    # Iterate over the operators and perform operations based on priority
    for priority in range(2, 0, -1):  # Check operations with descending priority
        for i in range(len(operators)):
            if operator_priority[operators[i]] == priority:
                # Perform operation based on the operator
                if operators[i] == '*':
                    result = (float(numbers[i]) * float(numbers[i + 1]))
                elif operators[i] == '/':
                    result = (float(numbers[i]) / float(numbers[i + 1]))
                elif operators[i] == '+':
                    result = (float(numbers[i]) + float(numbers[i + 1]))
                elif operators[i] == '-':
                    result = (float(numbers[i]) - float(numbers[i + 1]))

                # Update numbers and operators lists after the operation
                numbers[i] = result
                del numbers[i + 1]
                del operators[i]

    return numbers[0]  # Return the final result


def main():

    history = []

    print("[bold blue]\n******Welcome to Dipalo******\n[/bold blue]")

    expression = ''

    while expression.lower() != "exit":
        expression = input("Enter your expression: \n")

        # clean expression
        expression = clean_expression(expression)

        # create a new history expression with unique id
        unique_id = check_unique_id(history)

        history.append( {
            "id":unique_id,
            "expression":expression
        })

        if expression["error"] is not None:
            print("Illegal character found at index:", expression["error"])
            continue


    

if "__main__" == __name__:

    main()