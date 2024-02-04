import sys
import ntpath
import os

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# get cmd args
n = len(sys.argv)

if n < 0:
    raise Exception("Missing arguments. pass filename.asm as argument")

if n > 2:
    raise Exception("Too many arguments")

# get filename
filename = sys.argv[1]

static_var_name = path_leaf(filename)
static_var_name = static_var_name[0:len(filename)-3]

line_num_loop = 0
return_address_counter1 = 0

function_name_label_prepend = ""

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
    ins += process_function_call(function_name="Sys.init",num_args=0)

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
    temp = ""
    for i in range(0,len(data)):
        # skip comments
        if data[0] == "/":
            return None
        
        # skip white lines
        if len(data) == 1:
            return None
        
        if data[i] == "\n" or data[i] == " " or data[i] == "/" or data[i] == "\t":
            if temp == "push" or temp == "pop":
                segment, segment_num = get_segment_and_segment_num(data,i+1)
                return process_memory_access(
                    segment=segment,
                    segment_num=segment_num,
                    is_push=(temp == "push")
                )
            elif temp == "label" or temp == "goto" or temp == "if-goto":
                return process_branching(
                    data=data,
                    branch_op=temp,
                    start=i+1,
                    function_name=function_name_label_prepend
                )
            elif temp == "eq" or temp == "neg" or temp == "not" or temp == "add" or temp == "sub" or temp == "gt" or temp == "lt" or temp == "and" or temp == "or":
                return process_arithmetic(temp)
            elif temp ==  "function":
                function_name, num_vars = get_function_name_and_num_args(data=data,start=i+1)
                return process_function_declaration(function_name=function_name,num_vars=num_vars)
            elif temp == "call":
                function_name, num_args = get_function_name_and_num_args(data=data,start=i+1)
                return process_function_call(function_name=function_name,num_args=num_args)
            elif temp == "return":
                return process_function_return()
        else:
            temp += data[i]


"""
Purpose:
    process branching operations (goto, if-goto, label)

Arguments:
    data:
        string that contains label name

    branch_op:
        string that can be "goto", "if-goto" or "label" and used to determine branch operation

    start:
        index used to extract label name

Return:
    string that contains HACK assembly encoded instruction
"""
def process_branching(data,branch_op,start,function_name):
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

    if branch_op == "label":
        ins += f"//label {label_name}\n"
        ins += f"({label_name})\n"
    elif branch_op == "goto":
        ins += f"//goto @{label_name}\n"
        ins += f"@{label_name}\n"
        ins += "A=M\n"
        ins += "0;JMP\n"
    else:
        ins += f"// if-goto @{label_name}\n"
        # if label is if-goto NAME
        # then cond = pop()
        # if cond is True then jump
        # pop the stack
        ins += "@SP\n"
        ins += "M=M-1\n"
        ins += "@SP\n"
        ins += "A=M\n"
        # store popped value in D
        ins += "D=M\n"
        # goto label_name if D is True
        ins += f"@{label_name}\n"
        ins += "A=M\n"
        ins += "D;JGT\n"

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
    ins +=  "@LCL\n"
    ins += "D=M\n"
    ins += "@end_frame\n"
    ins += "M=D\n"

    # ret_address = *(end_frame - 5)
    ins += "@end_frame\n"
    ins += "D = M\n"
    ins += "@5\n"
    ins += "D = D - A\n"
    ins += "A = D\n"
    ins += "D = M\n"
    ins += "@ret_address\n"
    ins += "M = D\n"

    # *ARG = pop()
    ins += "@SP\n"
    ins += "M = M - 1\n"
    ins += "A = M\n"
    ins += "D = M\n"
    ins += "@ARG\n"
    ins += "A = M\n"
    ins += "M = D\n"

    # SP = ARG + 1
    ins += "@ARG\n"
    ins += "D = M + 1\n"
    ins += "@SP\n"
    ins += "M = D\n"

    # THAT = *(end_frame - 1)
    ins += "@end_frame\n"
    ins += "D = M - 1\n"
    ins += "A = D\n"
    ins += "D = M\n"
    ins += "@THAT\n"
    ins += "M = D\n"

    #THIS = *(end_frame - 2)
    ins += "@end_frame\n"
    ins += "D = M\n"
    ins += "@2\n"
    ins += "D = D - A\n"
    ins += "A = D\n"
    ins += "D = M\n"
    ins += "@THIS\n"
    ins += "M = D\n"
    
    #ARG = *(end_frame - 3)
    ins += "@end_frame\n"
    ins += "D = M\n"
    ins += "@3\n"
    ins += "D = D - A\n"
    ins += "A = D\n"
    ins += "D = M\n"
    ins += "@ARG\n"
    ins += "M = D\n"

    #LCL = *(end_frame - 4)
    ins += "@end_frame\n"
    ins += "D = M\n"
    ins += "@4\n"
    ins += "D = D - A\n"
    ins += "A = D\n"
    ins += "D = M\n"
    ins += "@LCL\n"
    ins += "M = D\n"

    # goto ret_address
    ins += "@ret_address\n"
    ins += "A = M\n"
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
    global function_name_label_prepend
    function_name_label_prepend = function_name
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
def process_function_call(function_name,num_args):
    global return_address_counter1
    return_address_label = f"{function_name}_{return_address_counter1}"
    return_address_counter1 += 1
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
    ins += f"@SP\n"
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
    process arithmetic instruction and turn it into HACK assembly

Arguments:
    op:
        string that represents opcode for arithmetic instruction

Return:
    ins:
        HACK assembly encoded instruction
"""
def process_arithmetic(op):
    ins = ""
    ins += f"//{op}\n"
    if op == "eq" or op == "neg" or op == "not":
        # a = pop stack
        # sp--
        ins += "// sp--\n"
        ins += "@SP\n"
        ins += "M=M-1\n"
        # *sp = popped value of stack
        # d = *sp
        ins += "// d=*sp\n"
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "D=M\n"
        if op == "eq":
            global line_num_loop
            ins += f"@L{line_num_loop}\n"
            ins += "D;JEQ\n"
            # push 0 to stack
            ins += "@0\n"
            ins += "D=A\n"
            ins += f"@L{line_num_loop+1}\n"
            ins += "0;JMP\n"
            # push 1 to stack
            ins += f"(L{line_num_loop})\n"
            ins += "@1\n"
            ins += "D=A\n"
            ins += f"(L{line_num_loop+1})\n"

            line_num_loop += 2
        elif op == "neg":
            # b = -a
            ins += "D=-D\n"
        elif op == "not":
            # b = !a
            ins += "D=!D\n"
        # push b
        # *sp = D
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "M=D\n"
        # sp++
        ins += "@SP\n"
        ins += "M=M+1\n"
    elif op == "add" or op == "sub" or op == "gt" or op == "lt" or op == "and" or op == "or":
        # a = pop stack
        # sp--
        ins += "@SP\n"
        ins += "M=M-1\n"
        # *sp = popped value of stack
        # d = *sp
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "D=M\n"
        # a = *sp
        ins += "@a\n"
        ins += "M=D\n"
        # b = pop stack
        # sp--
        ins += "@SP\n"
        ins += "M=M-1\n"
        # *sp = popped value of stack
        # d = *sp
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "D=M\n"
        # b = *sp
        ins += "@b\n"
        ins += "M=D\n"
        # load b
        ins += "@b\n"
        ins += "D=M\n"
        # load a
        ins += "@a\n"
        if op == "add":
            # c = a + b
            ins += "D=D+M\n"
        elif op == "sub":
            # c = a - b
            ins += "D=D-M\n"
        elif op == "and":
            # c = a & b
            ins += "D=D&M\n"
        elif op == "or":
            # c = a | b
            ins += "D=D|M\n"
        elif op == "gt" or op == "lt":
            # c = a > b
            # d = a - b
            ins += "D=D-M\n"
            # if (a-b) > 0 then a>b else b>a
            ins += f"@L{line_num_loop}\n"
            ins += "D;JGT\n"
            if op == "gt":
                # load 0 to stack
                ins += "@0\n"
                ins += "D=A\n"
                ins += f"@L{line_num_loop+1}\n"
                ins += "0;JMP\n"
                # load 1 to stack
                ins += f"(L{line_num_loop})\n"
                ins += "@1\n"
                ins += "D=A\n"
                ins += f"(L{line_num_loop+1})\n"
                
                line_num_loop += 2
            else:
                # load 1 to stack
                ins += "@1\n"
                ins += "D=A\n"
                ins += f"@L{line_num_loop+1}\n"
                ins += "0;JMP\n"
                # load 0 to stack
                ins += f"(L{line_num_loop})\n"
                ins += "@0\n"
                ins += "D=A\n"
                ins += f"(L{line_num_loop + 1})\n"

                line_num_loop += 2
        # push c
        # *sp = D
        ins += "@SP\n"
        ins += "A=M\n"
        ins += "M=D\n"
        # sp++
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
    Process memory access commands (push and pop)

Arguments:
    segment:
        memory segment to manipulate

    segmnet_num:
        integer which represents the index of the memory segment to manipulate

    is_push:
        boolean flag to determine if op is push or pop

Return:
    ins:
        hack assembly encoded instruction
"""
def process_memory_access(segment, segment_num,is_push):
    ins = ""
    ins += f"// {('push' if is_push else 'pop')} {segment} {segment_num}\n"
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

        if is_push:
            # *sp = *addr
            ins += "// *sp = *addr\n"
            ins += "@addr\n"
            ins += "A=M\n"
            ins += "D=M\n"
            ins += "@SP\n"
            ins += "A=M\n"
            ins += "M=D\n"

            # SP++
            ins += "// SP++\n"
            ins += "@SP\n"
            ins += "M=M+1\n"
        else:
            # SP--
            ins += "// SP--\n"
            ins += "@SP\n"
            ins += "M=M-1\n"
            
            # *addr = *sp
            ins += "// *addr = *sp\n"
            ins += "@SP\n"
            ins += "A=M\n"
            ins += "D=M\n"
            ins += "@addr\n"
            ins += "A=M\n"
            ins += "M=D\n"
    elif segment == "constant":
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
    elif segment == "static":
        #variables should be name filename.segment_num

        if is_push is False:
            # pop stack
            # sp --
            ins += "// SP-- \n"
            ins += "@SP\n"
            ins += "M=M-1\n"
            # var = *sp
            ins += "// var = *sp\n"
            ins += "@SP\n"
            ins += "A=M\n"
            ins += "D=M\n"
            # set variable value
            ins += "// set variable value\n"
            ins += f"@{static_var_name}.{segment_num}\n"
            ins += "M=D\n"
        else:
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

        if is_push:
            # *sp = *addr
            ins += "// *sp = *addr\n"
            ins += "@addr\n"
            ins += "A=M\n"
            ins += "D=M\n"
            ins += "@SP\n"
            ins += "A=M\n"
            ins += "M=D\n"

            # SP++
            ins += "// SP++\n"
            ins += "@SP\n"
            ins += "M=M+1\n"
        else:
            # SP--
            ins += "// SP--\n"
            ins += "@SP\n"
            ins += "M=M-1\n"
            
            # *addr = *sp
            ins += "// *addr = *sp\n"
            ins += "@SP\n"
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
        if is_push:
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
        else:
            # pop pointer 0/1
            # sp--,this/that=*sp

            # SP--
            ins += "// SP--\n"
            ins += "@SP\n"
            ins += "M=M-1\n"

            # this/that=*sp
            ins += "// this/that = *sp\n"
            ins += "@SP\n"
            ins += "A=M\n"
            ins += "D=M\n"
            ins += f"@{segment}\n"
            ins += "M=D\n"

    return ins

def process_file(input_file_name,output_file_name):
    # open input file
    with open(input_file_name,"r") as f:
        # get lines from input file
        for data in f:
            # process one line
            data = process_line(data)

            # ignore empty lines or comments
            if data is None:
                continue

            # write processed line to output file
            with open(output_file_name,"a+") as f2:
                f2.write(f"{data}\n")


is_dir = os.path.isdir(filename)

if os.path.isdir(filename) is True:
    dir_list = list(filter(lambda x: ".vm" in x,os.listdir(filename)))

    output_file_name = f"{filename}\{os.path.basename(os.path.dirname(filename))}.asm"

    with open(output_file_name,"a+") as f2:
        ins = bootstrap_code()
        f2.write(f"{ins}\n")

    
    for file in dir_list:
        filepath = f"{filename}\{file}"
        process_file(input_file_name=filepath,output_file_name=output_file_name)
else:
    # output file name
    filename2 = f"{filename[0:len(filename)-3]}.asm"

    process_file(input_file_name=filename,output_file_name=filename2)