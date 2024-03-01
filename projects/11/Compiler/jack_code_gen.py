"""
This module will generate p-code based on tokens
and the rules of the JACK language described in
the nand2tetris book
"""

import sys

class_symbol_table = {}
function_symbol_table = {}

field_count = 0
static_count = 0
arg_count = 0
local_count = 0
output_file = ""

def set_output_file(of):
    """
    Purpose:
        Set output file

    Arguments:
        of:
            output file name

    Return:
        None
    """
    global output_file
    output_file = of

def write_code(
    code
):
    """
    Purpose:
        Write code to output file

    Argument:
        code:
            code to write to file

    Return:
        None
    """
    global output_file
    with open(output_file,"a+") as f:
        f.write(f"{code}\n")

def generate_code_expression(exp,exp_type):
    """
    Purpose:
        Generate code for expression

    Argument:
        exp:
            expression to parse

        exp_type:
            type of expression
            can be:
                - number
                - variable
                - op
    Return:
        None
    """
    # check if type is int
    if exp_type == "number":
        write_code(
            code=f"push {exp}"
        )
    elif exp_type == "variable":
        write_code(
            code=f"push {exp}"
        )
    elif exp_typ == "op":
        write_code(
            code=
        )

def reset_symbol_table(
    is_class_level
):
    """
    Purpose:
        Reset symbol table

    Argument:
        is_class_level:
            boolean flag to determine if you 
            need to reset class or function
            symbol table

    Return:
        None
    """
    global class_symbol_table
    global function_symbol_table
    if is_class_level is True:
        class_symbol_table = {}
    elif is_class_level is False:
        function_symbol_table = {}


def add_to_symbol_table(
    name,
    id_type,
    kind,
    is_class_level
):
    """
    Purpose:
        Add entry to symbol table

    Argument:
        Name : str
            identifier name
            
        id_type : str
            data type of identifier
            it can be int, char, bool
            or a class

        kind : str
            kind of identifier
            For class it can be:
                - field
                - static
            For subprocedure it can be:
                - argument
                - local

        is_class_level : bool
            boolean flag that represents if we are dealing with class or subprocedure symbol table

    Return:
        None
    """
    global class_symbol_table
    global function_symbol_table
    global field_count, static_count
    global arg_count, local_count
    try:
        if is_class_level:
            assert name not in class_symbol_table
            assert kind == "field" or kind == "static"

            if kind == "field":
                class_symbol_table[name] = {
                    "type": id_type,
                    "kind": kind,
                    "num": field_count
                }
                field_count += 1
            elif kind == "static":
                class_symbol_table[name] = {
                    "type": id_type,
                    "kind": kind,
                    "num": static_count
                }
                static_count += 1
        else:
            assert name not in function_symbol_table
            assert kind == "argument" or kind == "local"
            if kind == "local":
                function_symbol_table[name] = {
                    "type": id_type,
                    "kind": kind,
                    "num": local_count
                }
                local_count += 1
            elif kind == "argument":
                function_symbol_table[name] = {
                    "type": id_type,
                    "kind": kind,
                    "num": arg_count
                }
                arg_count += 1
    except AssertionError:
        t = "class" if is_class_level else "subprocedure"
        print("Error: Identifier already in symbol table")
        print("OR invalid type or kind")
        print(f"Name: {name}")
        print(f"Type: {id_type}")
        print(f"Kind: {kind}")
        print(f"static count: {static_count}")
        print(f"argument count: {arg_count}")
        print(f"field count: {field_count}")
        print(f"local count:  {local_count}")
        print(f"Symbol table: {t}")
        sys.exit()
