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
    operators = re.findall(r'[+\-*/()]', expression)
    
    return numbers, operators

def clean_expression(expression):
    # Check for illegal characters using regular expression
    illegal_chars = re.findall(r'[^0-9.+\-*/()]', expression)
    
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
    # for i in range(1, len(expression) - 1):
    #     if expression[i] in '+-*/' and expression[i+1] in '+-*/':
    #         return {"expr": expression, "error": i}
    
    return {"expr": expression, "error": None}

def perform_operations(expression, steps):
    
    # separate nuumbers from operators in expression then get the numbers and operations from the expression

    nums, ops = separate_expression(expression)
    
    ops_priority = {'(':3, ')':3, '*':2, '/':2, '+':1, '-':1}
    new_nums = False

    while(len(nums) != 1):

        for crnt_op_priority in ops_priority:

            if new_nums:
                new_nums = False
                break

            for i, op in enumerate(ops):
                if op == crnt_op_priority:

                    oprand_1 = nums[i]
                    operand_2 = nums[i+1]

                    # determine if operator (op) is a '(' operator
                    if op == '(':
                        
                        # Find the innermost bracket
                        # start_index = expression.rfind('(')
                        # end_index = expression.index(')', start_index)

                        #  # Evaluate the expression inside the brackets
                        # bracket_expression = expression[start_index + 1:end_index]
                        # steps.append(f'({bracket_expression})')
                        # result, steps = perform_operations(bracket_expression, steps)

                        # del ops[i]
                        # del ops[len(ops) - ops[::-1].index(')') - 1]    
                        pass


                    else:
                        steps.append(f'{oprand_1}{op}{operand_2}')
                        result = str(eval(f'{oprand_1}{op}{operand_2}'))

                        del ops[i]
                        
                        del nums[i]
                        del nums[i]
                        nums.insert(i, result)
                        new_nums = True

                    break

    return result, steps      
      
def main():
    
    history = []

    print("[bold blue]\n******Welcome to Dipalo******\n[/bold blue]")

    crnt_expression = ''

    while True:

        crnt_expression = input("Enter your expression: \n")

        if crnt_expression.lower() == "exit":
            break

        elif crnt_expression.lower() == "history":

            if history:
                print('\nSelect number(i.e 1)')
                for i, h_item in enumerate(history, start=1):
                    print(f'{i}. {h_item["expression"]}')

                print('------------------')

                # get user selection
                selection = input()

                if selection == 'exit':
                    break
                
                item = history[int(selection)-1]

                print('\n------------------')
                print(f'expression: {item["expression"]}')
                print(f'result: {item["result"]}')
                print('------------------\n')

                
            else:
                print('\n[red]No History to show[/red]\n')
        
        else:

            # clean crnt_expression
            crnt_expression = clean_expression(crnt_expression)

            if crnt_expression["error"] is not None:
                print("Illegal character found at index:", crnt_expression["error"])
                continue

            # create a new history expression with unique id
            unique_id = check_unique_id(history)

            # make expression to be string again
            crnt_expression = crnt_expression["expr"]


            result = perform_operations(crnt_expression, [])

            history.append( {
                "id":unique_id,
                "expression":crnt_expression,
                "steps":result[1],
                "result":result[0]
            })

            print("-------------")
            print(result[0]+'\n')
            # print(result[1])

if "__main__" == __name__:

    main()