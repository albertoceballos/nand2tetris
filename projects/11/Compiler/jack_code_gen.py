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
label_count = 0

class_name = ""

def get_class_name():
    """
    Purpose:
        Return class name

    Arguments:
        None

    Return:
        class name : str
    """
    global class_name
    return class_name

def set_class_name(n):
    """
    Purpose:
        Set class name

    Arguments:
        n : str
            name of class

    Return:
        None
    """
    try:
        global class_name
        assert isinstance(n,str)
        class_name = n
    except AssertionError:
        print("Error: ")
        print("Invalid argument")
        print(f"n = {n}")
        sys.exit()

def write_push_pop(
    segment,
    index,
    is_push
):
    """
    Purpose:
        Write push or pop command

    Argument:
        segment : str
            memory segment to manipulate
            Can be one of the following:
                - const
                - arg
                - local
                - static
                - this
                - that
                - pointer
                - temp

        index : int
            index of memory segment to manipulate

        is_push : boolean
            boolean flag to determine if operation is push or pop
    """
    try:
        assert isinstance(is_push,bool)
        assert isinstance(segment,str)
        assert segment in ("const","arg","local","static","this","that","pointer","temp")
        assert isinstance(index,int)
        assert index >= 0
        segment = segment.upper()
        if is_push is True:
            write_code(code=f"push {segment} {index}")
        else:
            write_code(code=f"pop {segment} {index}")
    except AssertionError:
        print("Error: Received invalid arguments")
        print(f"segment = {segment}")
        print(f"index = {index}")
        print(f"is_push = {is_push}")
        sys.exit()

def write_arithmetic_op(op):
    """
    Purpose:
        Write arithmetic operation

    Arguments:
        op : str
            operation to perform.
            Can be one of the following:
                - add
                - sub
                - neg
                - eq
                - gt
                - lt
                - and
                - or
                - not
    Return:
        None
    """
    try:
        assert isinstance(op,str)
        assert op in ("add","sub","neg","eq","gt","lt","and","or","not")
        write_code(f"{op}")
    except AssertionError:
        print("Invalid operation")
        print(f"operation = {op}")
        sys.exit()

def get_label():
    """
    Purpose:
        Gets unique label
    
    Arguments:
        None

    Return:
        i : int
            unique label
    """
    global label_count
    i = label_count
    label_count += 1
    return i

def write_label(
    label_type,
    label_id
):
    """
    Purpose:
        Write label for if statements or loops

    Arguments:
        label_type : str
            can be one of the following:
                - goto
                - if-goto
                - label

        label_id : int
            unique label id
    Return:
        None
    """
    try:
        assert isinstance(label_type,str)
        assert label_type in ("goto","if-goto","label")
        assert isinstance(label_id,int)
        assert label_id >= 0

        if label_type == "label":
            write_code(f"L{label_id}")
        elif label_type == "goto":
            write_code(f"goto L{label_id}")
        else:
            write_code(f"if-goto L{label_id}")
    except AssertionError:
        print("Invalid arguments")
        print(f"label_type = {label_type}")
        print(f"label_id = {label_id}")
        sys.exit()

def write_function_call(
    function_name,
    num_args
):
    """
    Purpose:
        Write function call
    
    Arguments:
        function_name : str
            function name

        num_args : int
            number of arguments

    Return:
        None
    """
    try:
        assert isinstance(function_name,str)
        assert isinstance(num_args,int)
        assert num_args >= 0
        write_code(f"call {function_name} {num_args}")
    except AssertionError:
        print("Error: ")
        print("Invalid arguments")
        print(f"function_name: {function_name}")
        print(f"num_args = {num_args}")
        sys.exit()

def set_output_file(of):
    """
    Purpose:
        Set output file

    Arguments:
        of : str
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
        code : str
            code to write to file

    Return:
        None
    """
    try:
        assert isinstance(code,str)
        global output_file
        with open(output_file,"a+",encoding="utf-8") as f:
            f.write(f"{code}\n")
    except AssertionError:
        print("Error: Invalid arguments")
        print(f"code = {code}")
        sys.exit()

def reset_symbol_table(
    is_class_level
):
    """
    Purpose:
        Reset symbol table

    Argument:
        is_class_level : bool
            boolean flag to determine if you 
            need to reset class or function
            symbol table

    Return:
        None
    """
    try:
        assert isinstance(isinstance,bool)
        global class_symbol_table
        global function_symbol_table
        if is_class_level is True:
            class_symbol_table = {}
        elif is_class_level is False:
            function_symbol_table = {}
    except AssertionError:
        print("Invalid arguments")
        print(f"is_class_level = {is_class_level}")
        sys.exit()

def get_symbol_from_table(name):
    """
    Purpose:
        retrieve symbol from table

    Arguments:
        name : str
            variable name in symbol table

    Return:
        variable name
    """
    try:
        assert isinstance(name,str)
        assert name in function_symbol_table or name in class_symbol_table
        if name in function_symbol_table:
            return function_symbol_table[name]
        elif name in class_symbol_table:
            return class_symbol_table[name]
    except AssertionError:
        print("Error: ")
        print("Invalid argument OR symbol not found")
        print(f"name={name}")
        sys.exit()
    

def add_to_symbol_table(
    name,
    id_type,
    kind,
    var_classification,
    is_class_level
):
    """
    Purpose:
        Add entry to symbol table

    Argument:
        name : str
            identifier name
            
        id_type : str
            data type of identifier
            it can be int, char, bool
            or a class

        kind : str
            kind of identifier
            For variables inside a class it can be:
                - field
                - static
            For variables inside a subprocedure it can be:
                - argument
                - local
            For a constructor or method or function:
                - none

        var_classification : str
            variable classification
            it can be:
                - variable
                - object
                - function
                - method
                - class

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
        assert isinstance(name,str)
        assert isinstance(id_type,str)
        assert isinstance(kind,str)
        assert isinstance(var_classification,str)
        assert kind in ("field","static","argument","local","none")
        assert var_classification in ("variable","object","function","method","class")
        assert isinstance(is_class_level,bool)

        if is_class_level:
            assert name not in class_symbol_table
            assert kind == "field" or kind == "static"

            if kind == "field":
                class_symbol_table[name] = {
                    "type": id_type,
                    "kind": kind,
                    'var_classification': var_classification,
                    "num": field_count
                }
                field_count += 1
            elif kind == "static":
                class_symbol_table[name] = {
                    "type": id_type,
                    "kind": kind,
                    'var_classification': var_classification,
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
                    'var_classification': var_classification,
                    "num": local_count
                }
                local_count += 1
            elif kind == "argument":
                function_symbol_table[name] = {
                    "type": id_type,
                    "kind": kind,
                    'var_classification': var_classification,
                    "num": arg_count
                }
                arg_count += 1
    except AssertionError:
        t = "class" if is_class_level else "subprocedure"
        print("Error: Identifier already in symbol table")
        print("OR invalid type or kind")
        print("OR invalid argument")
        print(f"Name: {name}")
        print(f"Type: {id_type}")
        print(f"Kind: {kind}")
        print(f"static count: {static_count}")
        print(f"argument count: {arg_count}")
        print(f"field count: {field_count}")
        print(f"local count:  {local_count}")
        print(f"Symbol table: {t}")
        sys.exit()
