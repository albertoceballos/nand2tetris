import sys
import os

# get cmd args
n = len(sys.argv)

if n < 0:
    raise Exception("Missing arguments. pass filename.asm as argument")

if n > 2:
    raise Exception("Too many arguments")

# get filename
line_num_loop = 0
return_address_counter = 0
function_name = ""

"""
Purpose:
    write bootstrap code for HACK assembler
    the bootstrap code sets SP=256 and calls Sys.init
    Sys.init is the entry function and every VM program should have it
    This is basically the main function in other prog languages

Argument:
    None

Return:
    HACK encoded instruction
"""
def bootstrap_code():
    # set SP = 256
    ins = "//bootstrap code\n"
    ins += "@256\n"
    ins += "D = A\n"
    ins += "@SP\n"
    ins += "M = D\n"

    # call Sys.init
    ins += process_function_call(function_name="Sys.init",num_args=0,return_address_counter1=0)
    global return_address_counter
    return_address_counter += 1
    return ins

"""
Purpose:
    process line extracted from vm file

Argument:
    data:
        string that contains instruction

Return:
    None if comment or empty line
    Otherwise it will return the HACK assembly encoded instruction
"""
def process_line(data):
    global line_num_loop
    global function_name
    global return_address_counter
    temp = ""
    for i in range(0,len(data)):
        # skip comments
        if data[0] == "/":
            return None
        
        # skip white lines
        if len(data) == 1:
            return None
        
        if data[i] == "\n" or data[i] == " " or data[i] == "/" or data[i] == "\t":
            if temp == "push":
                segment, segment_num = get_segment_and_segment_num(data,i+1)
                return process_push(
                    segment=segment,
                    segment_num=segment_num
                )
            elif temp == "pop":
                segment, segment_num = get_segment_and_segment_num(data,i+1)
                return process_pop(
                    segment=segment,
                    segment_num=segment_num
                )
            elif temp == "label":
                fn = function_name
                return process_label(
                    data=data,
                    start=i+1,
                    function_name=fn
                )
            elif temp == "if-goto":
                fn = function_name
                return process_if_goto(
                    data=data,
                    start=i+1,
                    function_name=fn
                )
            elif temp == "goto":
                fn = function_name
                return process_goto(
                    data=data,
                    start=i+1,
                    function_name=fn
                )
            elif temp == "add":
                return process_add()
            elif temp == "sub":
                return process_sub()
            elif temp == "neg":
                return process_neg()
            elif temp == "not":
                return process_not()
            elif temp == "and":
                return process_and()
            elif temp == "or":
                return process_or()
            elif temp == "gt":
                a = process_gt()
                line_num_loop += 1
                return a
            elif temp == "lt":
                a = process_lt()
                line_num_loop += 1
                return a
            elif temp == "eq":
                a = process_eq()
                line_num_loop += 1
                return a
            elif temp ==  "function":
                function_name1, num_vars = get_function_name_and_num_args(data=data,start=i+1)
                function_name = function_name1
                return process_function_declaration(function_name=function_name1,num_vars=num_vars)
            elif temp == "call":
                function_name, num_args = get_function_name_and_num_args(data=data,start=i+1)
                a = process_function_call(function_name=function_name,num_args=num_args,return_address_counter1=return_address_counter)
                return_address_counter += 1
                return a
            elif temp == "return":
                return process_function_return()
        else:
            temp += data[i]

"""
Purpose:
    Process label

Arguments:
    data:
        data to parse

    start:
        starting index to parse

    function_name:
        string that contains function name

Return:
    HACK coded instruction
"""
def process_label(data,start,function_name):
    # label name
    label_name = ""
    # labels in functions should follow format function_name$label_name
    if len(function_name) > 0:
        label_name = f"{function_name}$"

    # iterate over string
    for i in range(start,len(data)):
        # when you reach the space you find the label name
        if data[i] == " " or data[i] == "\n" or data[i] == "/":
            break
        else:
            label_name += data[i]

    ins = ""
    ins += f"//label {label_name}\n"
    ins += f"({label_name})\n"

    return ins

"""
Purpose:
    Process if goto

Arguments:
    data:
        data to parse

    start:
        starting index to parse

    function_name:
        string that contains function name

Return:
    HACK coded instruction
"""
def process_if_goto(data,start,function_name):
    # label name
    label_name = ""
    # labels in functions should follow format function_name$label_name
    if len(function_name) > 0:
        label_name = f"{function_name}$"

    # iterate over string
    for i in range(start,len(data)):
        # when you reach the space you find the label name
        if data[i] == " " or data[i] == "\n" or data[i] == "/":
            break
        else:
            label_name += data[i]

    ins = ""
    ins += f"// if-goto @{label_name}\n"
    # if label is if-goto NAME
    # then cond = pop()
    # if cond is True then jump
    # pop the stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n"
    # store popped value in D
    ins += "D=M\n"
    # goto label_name if D is True
    ins += f"@{label_name}\n"
    ins += "D;JNE\n"

    return ins

"""
Purpose:
    Process goto

Arguments:
    data:
        data to parse

    start:
        starting index to parse

    function_name:
        string that contains function name

Return:
    HACK coded instruction
"""
def process_goto(data,start,function_name):
    # label name
    label_name = ""
    # labels in functions should follow format function_name$label_name
    if len(function_name) > 0:
        label_name = f"{function_name}$"

    # iterate over string
    for i in range(start,len(data)):
        # when you reach the space you find the label name
        if data[i] == " " or data[i] == "\n" or data[i] == "/":
            break
        else:
            label_name += data[i]

    ins = ""
    ins += f"//goto @{label_name}\n"
    ins += f"@{label_name}\n"
    ins += "0;JMP\n"

    return ins

"""
Purpose:
    process function return

Argument:
    None

Return:
    HACK encoded instruction
"""
def process_function_return():
    """
    end_frame = LCL
    ret_address = *(end_frame - 5)
    *ARG = pop()
    SP = ARG+1
    THAT = *(end_frame - 1)
    THIS = *(end_frame - 2)
    ARG = *(end_frame - 3)
    LCL = *(end_frame - 4)
    goto ret_address
    """
    ins = "// process function return\n"

    # end_frame = LCL
    ins += "@LCL\n"
    ins += "D=M\n"
    ins += "@end_frame\n"
    ins += "M=D\n"

    # ret_address = *(end_frame - 5)
    ins += "@5\n"
    ins += "D=D-A\n"
    ins += "A=D\n"
    ins += "D=M\n"
    ins += "@ret_address\n"
    ins += "M=D\n"

    # *ARG = pop()
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n"
    ins += "D=M\n"
    ins += "@ARG\n"
    ins += "A=M\n"
    ins += "M=D\n"

    # SP = ARG + 1
    ins += "@ARG\n"
    ins += "D=M+1\n"
    ins += "@SP\n"
    ins += "M=D\n"

    # THAT = *(end_frame - 1)
    ins += "@end_frame\n"
    ins += "D=M\n"
    ins += "@1\n"
    ins += "D=D-A\n"
    ins += "A=D\n"
    ins += "D=M\n"
    ins += "@THAT\n"
    ins += "M=D\n"

    #THIS = *(end_frame - 2)
    ins += "@end_frame\n"
    ins += "D=M\n"
    ins += "@2\n"
    ins += "D=D-A\n"
    ins += "A=D\n"
    ins += "D=M\n"
    ins += "@THIS\n"
    ins += "M=D\n"
    
    #ARG = *(end_frame - 3)
    ins += "@end_frame\n"
    ins += "D=M\n"
    ins += "@3\n"
    ins += "D=D-A\n"
    ins += "A=D\n"
    ins += "D=M\n"
    ins += "@ARG\n"
    ins += "M=D\n"

    #LCL = *(end_frame - 4)
    ins += "@end_frame\n"
    ins += "D=M\n"
    ins += "@4\n"
    ins += "D=D-A\n"
    ins += "A=D\n"
    ins += "D=M\n"
    ins += "@LCL\n"
    ins += "M=D\n"

    # goto ret_address
    ins += "@ret_address\n"
    ins += "A=M\n"
    ins += "0;JMP\n"

    return ins


"""
Purpose:
    process function declaration

Argument:
    function_name:
        name of function

    num_vars:
        number of local variables

Return:
    HACK encoded instruction
"""
def process_function_declaration(function_name,num_vars):
    """
    (function_name)
    repeat num_vars times:
        push 0
    """
    ins = f"// function declaration {function_name} with {num_vars}\n"
    # (function name)
    ins += f"({function_name})\n"
    # push 0 num_vars times
    for _ in range(0,num_vars):
        ins += "@0\n"
        ins += "D=A\n"
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "M=D\n"
        ins += "@SP\n"
        ins += "M=M+1\n"

    return ins

"""
Purpose:
    Handle call
    calls the function
    creates function frame

Arguments:
    function_name:
        string that contains function name

    num_args:
        number of arguments to pass to function

Return:
    HACK encoded instruction
"""
def process_function_call(function_name,num_args,return_address_counter1):
    return_address_label = f"{function_name}_ret_{return_address_counter1}"
    """
    push return adress
    push LCL
    push ARG
    push THIS
    push THAT
    ARG = SP-5-num_args
    LCL = SP
    goto function_name
    (return address)
    """
    ins = f"// process function call {function_name} with args {num_args}\n"
    # push return address
    ins += f"// push return address label {return_address_label}\n"
    ins += push_mem_address_to_stack(return_address_label)
    # push LCL
    ins += "//push LCL\n"
    ins += push_mem_address_to_stack("LCL")
    # push arg
    ins += "// push ARG\n"
    ins += push_mem_address_to_stack("ARG")
    # push this
    ins += "// push THIS\n"
    ins += push_mem_address_to_stack("THIS")
    # push that
    ins += "// push THAT\n"
    ins += push_mem_address_to_stack("THAT")
    # ARG = SP-5-num_args
    ins += "// ARG = SP - 5 - num_args\n"
    ins += "@SP\n"
    ins += "D=M\n"
    ins += "@5\n"
    ins += "D=D-A\n"
    ins += f"@{num_args}\n"
    ins += "D=D-A\n"
    ins += "@ARG\n"
    ins += "M=D\n"
    # LCL = SP
    ins += "// LCL = SP\n"
    ins += "@SP\n"
    ins += "D=M\n"
    ins += "@LCL\n"
    ins += "M=D\n"

    # goto function_name
    ins += f"// goto {function_name}\n"
    ins += f"@{function_name}\n"
    ins += "0;JMP\n"

    ins += f"({return_address_label})\n"

    return ins


"""
Purpose:
    push memory address to stack

Argument:
    memory_address:
        string that represents memory address to push

Return:
    HACK encoded instruction
"""
def push_mem_address_to_stack(memory_address):
    # push mem => *sp = address, sp++
    ins = f"@{memory_address}\n"
    if memory_address == "LCL" or memory_address == "ARG" or memory_address == "THIS" or memory_address == "THAT":
        ins += "D=M\n"
    else:
        ins += "D=A\n"
    ins += "@SP\n"
    ins += "A=M\n"
    ins += "M=D\n"
    ins += "@SP\n"
    ins += "M=M+1\n"
    return ins




"""
Purpose:
    Retrieve function name and number of arguments from string

Arguments:
    data:
        string that contains the VM instruction that has the function name and num args

    start:
        index from which to start processing string

Return:
    function_name:
        string that contains function name

    num_args:
        int that represents number of arguments
"""
def get_function_name_and_num_args(data,start):
    # temp variables
    function_name = ""
    num_args = -1
    temp = ""
    # iterate over string
    for i in range(start,len(data)):
        # when you reach the space you find function name
        if data[i] == " " or data[i] == "\n" or data[i] == "/":
            if function_name == "":
                function_name = temp
                temp = ""
            else:
                num_args = int(temp)
                break
        else:
            temp += data[i]

    return function_name, num_args

"""
Purpose:
    Process add instruction

Arguments:
    None

Return:
    HACK coded instruction
"""
def process_add():
    ins = "// add\n"
    # sp-- (stack pop)
    ins += "@SP\n"
    ins += "M=M-1\n"
    # *sp = popped value of stack
    # d = *sp
    ins += "A=M\n" #follow pointer
    ins += "D=M\n" #D = b
    # sp -- (stack pop)
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n" # follow pointer
    ins += "M=D+M\n" #M[a] = b + M[a]
    # sp++ (stack push)
    ins += "@SP\n"
    ins += "M=M+1\n"
    
    return ins

"""
Purpose:
    Process add instruction

Arguments:
    None

Return:
    HACK coded instruction
"""
def process_sub():
    ins = "// sub\n"
    # sp-- (stack pop)
    ins += "@SP\n"
    ins += "M=M-1\n"
    # *sp = popped value of stack
    # d = *sp
    ins += "A=M\n" #follow pointer
    ins += "D=M\n" #D = b
    # sp -- (stack pop)
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n" # follow pointer
    ins += "M=M-D\n" #M[a] = b + M[a]
    # sp++ (stack push)
    ins += "@SP\n"
    ins += "M=M+1\n"
    
    return ins

"""
Purpose:
    Process add instruction

Arguments:
    None

Return:
    HACK coded instruction
"""
def process_neg():
    ins = "// process neg\n"
    # sp-- (stack pop)
    ins += "@SP\n"
    ins += "M=M-1\n"

    # *sp = popped value of stack
    # d = *sp
    ins += "A=M\n" #follow pointer
    ins += "D=-M\n" #D = -a
    ins += "M=D\n" # write data to memory location
    # sp++ (stack push)
    ins += "@SP\n"
    ins += "M=M+1\n"

    return ins

"""
Purpose:
    Process NOT instruction

Arguments:
    None

Return:
    HACK coded instruction
"""
def process_not():
    ins = "// process not"
    # sp-- (stack pop)
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n" # follow pointer
    ins += "D=!M\n" # NOT(value)
    ins += "M=D\n" # write value
    ins += "@SP\n"
    ins += "M=M+1\n"

    return ins

"""
Purpose:
    Process AND instruction

Arguments:
    None

Return:
    HACK coded instruction
"""
def process_and():
    ins = "// process and\n"
    # pop stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    # follow pointer
    ins += "A=M\n"
    # D = A
    ins += "D=M\n"
    # pop stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n" # follow pointer
    # and operation = A & B
    ins += "D=D&M\n"
    # write result to memory
    ins += "M=D\n"
    # push stack
    ins += "@SP\n"
    ins += "M=M+1\n"
    return ins

"""
Purpose:
    Process OR instruction

Arguments:
    None

Return:
    HACK coded instruction
"""
def process_or():
    ins = "// process or\n"
    # pop stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    # follow pointer
    ins += "A=M\n"
    # D = A
    ins += "D=M\n"
    # pop stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n" # follow pointer
    # and operation = A & B
    ins += "D=D|M\n"
    # write result to memory
    ins += "M=D\n"
    # push stack
    ins += "@SP\n"
    ins += "M=M+1\n"
    return ins

"""
Purpose:
    Process EQ instruction

Arguments:
    None

Return:
    HACK coded instruction
"""
def process_eq():
    ins = "// process eq\n"
    # pop stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    # follow pointer
    ins += "A=M\n"
    # get first value
    ins += "D=M\n"
    # pop stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    # follow pointer
    ins += "A=M\n"
    # get second value and subtract them first-second
    ins += "D=D-M\n"
    # if they are equal then jump to EQUAL label
    ins += f"@EQUAL_{line_num_loop}\n"
    ins += "D;JEQ\n"
    # if they are not equal then jump to FINAL label with D=0
    ins += "D=0\n"
    ins += f"@FINAL_{line_num_loop}\n"
    ins += "0;JEQ"
    # set D=-1 in EQUAL label
    ins += f"(EQUAL_{line_num_loop})\n"
    ins += "D=-1\n"
    # set value of *sp
    ins += f"(FINAL_{line_num_loop})\n"
    ins += "@SP\n"
    ins += "A=M\n" # follow pointer
    ins += "M=D\n" # write data
    # push stack (sp++)
    ins += "@SP\n"
    ins += "M=M+1\n"

    return ins

"""
Purpose:
    Process GT instruction

Arguments:
    None

Return:
    HACK coded instruction
"""
def process_gt():
    ins = "// process GT\n"
    # pop  stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n" # follow pointer
    ins += "D=M\n" # store first value in D
    # pop stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n" # follow pointer
    # subtract second from first
    ins += "D=M-D\n"
    # go to GREATER_THAN label if res > 0
    ins += f"@GREATER_THAN_{line_num_loop}\n"
    ins += "D;JGT\n"
    # jump to END label
    ins += "D=0\n"
    ins += f"@END_{line_num_loop}\n"
    ins += "0;JEQ\n"
    # GREATER_THAN label which sets D=-1
    ins += f"(GREATER_THAN_{line_num_loop})\n"
    ins += "D=-1\n"
    # END label
    ins += f"(END_{line_num_loop})\n"
    ins += "@SP\n"
    ins += "A=M\n"
    ins += "M=D\n"
    # push to stack (sp++)
    ins += "@SP\n"
    ins += "M=M+1\n"

    return ins

"""
Purpose:
    Process LT instruction

Arguments:
    None

Return:
    HACK coded instruction
"""
def process_lt():
    ins = "// process lt\n"

    # pop stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n" # follow pointer
    # store first value
    ins += "D=M\n"
    # pop stack
    ins += "@SP\n"
    ins += "M=M-1\n"
    ins += "A=M\n" # follow pointer
    # second - first
    ins += "D=M-D\n"
    # jump to LESS_THAN label if res < 0
    ins += f"@LESS_THAN_{line_num_loop}\n"
    ins += "D;JLT\n"
    # jump to END label
    ins += "D=0\n"
    ins += f"@END_{line_num_loop}\n"
    ins += "0;JEQ\n"
    # LESS THAN label
    ins += f"(LESS_THAN_{line_num_loop})\n"
    ins += "D=-1\n"
    # END label
    ins += f"(END_{line_num_loop})\n"
    # write data
    ins += "@SP\n"
    ins += "A=M\n"
    ins += "M=D\n"
    # push to stack
    ins += "@SP\n"
    ins += "M=M+1\n"
    return ins

"""
Purpose:
    Get segment and segment number from string

Argument:
    data:
        string that contains instruction

    start:
        index to start processing from

Return:
    segment and segment_num
"""
def get_segment_and_segment_num(data,start):
    # temp variables
    segment = ""
    segment_num = -1
    temp = ""
    # iterate over string
    for i in range(start,len(data)):
        # when you reach the space you find segment
        if data[i] == " " or data[i] == "\n" or data[i] == "/":
            if segment == "":
                segment = temp
                temp = ""
            else:
                segment_num = int(temp)
                break
        else:
            temp += data[i]

    return segment, segment_num

"""
Purpose:
    process push operation

Arguments:
    segment:
        memory segment to manipulate

    segmnet_num:
        integer which represents the index of the memory segment to manipulate

Return:
    ins:
        hack assembly encoded instruction
"""
def process_push(segment,segment_num):
    global static_var_name
    ins = ""
    ins += f"// push {segment} {segment_num}\n"
    if segment == "constant":
        ins += "//*sp=i\n"
        # *sp = i
        ins += f"@{segment_num}\n"
        ins += "D=A\n"
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "M=D\n"

        # SP++
        ins += "//*SP++\n"
        ins += "@SP\n"
        ins += "M=M+1\n"
    elif segment == "local" or segment == "argument" or segment == "this" or segment == "that":
        if segment == "local":
            segment = "LCL"
        elif segment == "argument":
            segment = "ARG"
        elif segment == "this":
            segment = "THIS"
        elif segment == "that":
            segment = "THAT"

        ins += "// addr = segment_pointer + segment_num\n"
        ins += f"@{segment_num}\n"
        ins += "D=A\n"
        ins += f"@{segment}\n"
        ins += "A=D+M\n"

        # *sp = *addr
        ins += "// *sp = *addr\n"
        #ins += "@addr\n"
        #ins += "A=M\n"
        ins += "D=M\n"
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "M=D\n"

        # SP++
        ins += "// SP++\n"
        ins += "@SP\n"
        ins += "M=M+1\n"
    elif segment == "temp":
        # compute addr
        # addr = 5 + segment_num
        ins += "// addr = 5 + segment_num\n"
        ins += "@5\n"
        ins += "D=A\n"
        ins += f"@{segment_num}\n"
        #ins += "D=D+A\n"
        #ins += "@addr\n"
        #ins += "M=D\n"
        ins += "A=D+A\n"
        # *sp = *addr
        ins += "// *sp = *addr\n"
        #ins += "@addr\n"
        #ins += "A=M\n"
        ins += "D=M\n"
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "M=D\n"

        # SP++
        ins += "// SP++\n"
        ins += "@SP\n"
        ins += "M=M+1\n"
    elif segment == "pointer":
        if segment_num == 0:
            segment = "THIS"
        else:
            segment = "THAT"
        # push pointer 0/1
        # *sp=this/that,SP++
        # *sp = this
        ins += "// *sp = this\n"
        ins += f"@{segment}\n"
        ins += "D=M\n"
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "M=D\n"
        # SP++
        ins += "// SP++\n"
        ins += "@SP\n"
        ins += "M=M+1\n"
    elif segment == "static":
        # push stack
        # get variable value
        ins += "// get variable value\n"
        ins += f"@{static_var_name}.{segment_num}\n"
        ins += "D=M\n"
        # *sp = var value
        ins += "// *sp = var value\n"
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "M=D\n"
        # sp++
        ins += "// SP++\n"
        ins += "@SP\n"
        ins += "M=M+1\n"

    return ins
        
"""
Purpose:
    process pop operation

Arguments:
    segment:
        memory segment to manipulate

    segmnet_num:
        integer which represents the index of the memory segment to manipulate

Return:
    ins:
        hack assembly encoded instruction
"""
def process_pop(segment,segment_num):
    global static_var_name
    ins = ""
    ins += f"// pop {segment} {segment_num}\n"
    if segment == "local" or segment == "argument" or segment == "this" or segment == "that":
        if segment == "local":
            segment = "LCL"
        elif segment == "argument":
            segment = "ARG"
        elif segment == "this":
            segment = "THIS"
        elif segment == "that":
            segment = "THAT"

        # compute addr
        # addr = segment pointer + segment_num
        ins += "// addr = segment_pointer + segment_num\n"
        ins += f"@{segment_num}\n"
        ins += "D=A\n"
        ins += f"@{segment}\n"
        ins += "D=D+M\n"
        ins += "@addr\n"
        ins += "M=D\n"
        # SP--
        ins += "// SP--\n"
        ins += "@SP\n"
        ins += "M=M-1\n"
        
        # *addr = *sp
        ins += "// *addr = *sp\n"
        ins += "A=M\n"
        ins += "D=M\n"
        ins += "@addr\n"
        ins += "A=M\n"
        ins += "M=D\n"
    elif segment == "temp":
        # compute addr
        # addr = 5 + segment_num
        ins += "// addr = 5 + segment_num\n"
        ins += "@5\n"
        ins += "D=A\n"
        ins += f"@{segment_num}\n"
        ins += "D=D+A\n"
        ins += "@addr\n"
        ins += "M=D\n"
        # SP--
        ins += "// SP--\n"
        ins += "@SP\n"
        ins += "M=M-1\n"
        
        # *addr = *sp
        ins += "// *addr = *sp\n"
        ins += "A=M\n"
        ins += "D=M\n"
        ins += "@addr\n"
        ins += "A=M\n"
        ins += "M=D\n"
    elif segment == "pointer":
        if segment_num == 0:
            segment = "THIS"
        else:
            segment = "THAT"
        # push pointer 0/1
        # *sp=this/that,SP++
        # pop pointer 0/1
        # sp--,this/that=*sp

        # SP--
        ins += "// SP--\n"
        ins += "@SP\n"
        ins += "M=M-1\n"

        # this/that=*sp
        ins += "// this/that = *sp\n"
        ins += "A=M\n"
        ins += "D=M\n"
        ins += f"@{segment}\n"
        ins += "M=D\n"
    elif segment == "static":
        #variables should be name filename.segment_num
        # pop stack
        # sp --
        ins += "// SP-- \n"
        ins += "@SP\n"
        ins += "M=M-1\n"
        # var = *sp
        ins += "// var = *sp\n"
        ins += "A=M\n"
        ins += "D=M\n"
        # set variable value
        ins += "// set variable value\n"
        ins += f"@{static_var_name}.{segment_num}\n"
        ins += "M=D\n"

    return ins
        
def process_file(input_file_name,output_file_name):
    global function_name
    # open input file
    with open(input_file_name,"r") as f:
        # get lines from input file
        for data in f:
            # process one line
            data = process_line(data)

            function_name = ""

            # ignore empty lines or comments
            if data is None:
                continue

            # write processed line to output file
            with open(output_file_name,"a+") as f2:
                f2.write(f"{data}\n")

filename = sys.argv[1]
is_dir = os.path.isdir(filename)

if os.path.isdir(filename) is True:
    dir_name = sys.argv[1]

    output_file_name = f"{dir_name}/{dir_name.split('/')[-1]}.asm"

    with open(output_file_name,"a+") as f2:
        ins = bootstrap_code()
        f2.write(f"{ins}\n")

    for file in os.listdir(dir_name):
        if file.endswith(".vm"):
            filepath = f"{filename}/{file}"
            file = file.split(".")[0]
            static_var_name = file

            process_file(input_file_name=filepath,output_file_name=output_file_name)
else:
    filename = sys.argv[1]
    filename = filename.split('/')[-1].split('.')[0]
    input_file = sys.argv[1]
    # output file name
    filename2 = f"{filename}.asm"
    static_var_name = filename

    process_file(input_file_name=input_file,output_file_name=filename2)