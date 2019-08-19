import sys
import math

def get_arg(arg: str, operations: list) -> int:
    if arg.startswith("$"):
        return calc_cell(int(arg[1:]), operations)
    else:
        return int(arg)

def calc_cell(i: int, operations: list) -> int:
    operation_name, arg1, arg2 = operations[i]
    if operation_name == "VALUE":
        return int(get_arg(arg1, operations))
    else:
        arg1, arg2 = get_arg(arg1, operations), get_arg(arg2, operations)
        if operation_name == "ADD":
            value = arg1 + arg2
        elif operation_name == "SUB":
            value = arg1 - arg2
        elif operation_name == "MULT":
            value = arg1 * arg2
        operations[i] = ("VALUE", str(value), "_")
        return value

n = int(input())
operations = [input().split() for _ in range(n)]
for i in range(n):
    print(calc_cell(i, operations))
