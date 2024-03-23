import re

def separate_expression(expression):
    # Using regular expression to split numbers and operators
    numbers = re.findall(r'[0-9.]+', expression)
    operators = re.findall(r'[+\-*/]', expression)
    
    return numbers, operators

expression = "1+5/5*1"
numbers, operators = separate_expression(expression)
result = (numbers, operators)
# print(result)


def main():
    pass

if "__main__" == __name__:

    main()