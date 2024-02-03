import sys
import ntpath

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
                    start=i+1
                )
            elif temp == "eq" or temp == "neg" or temp == "not" or temp == "add" or temp == "sub" or temp == "gt" or temp == "lt" or temp == "and" or temp == "or":
                return process_arithmetic(temp)
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
def process_branching(data,branch_op,start):
    # label name
    label_name = ""
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
        ins += "D;JGT\n"

    return ins


        

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

# output file name
filename2 = f"{filename[0:len(filename)-3]}.asm"

# open input file
with open(filename,"r") as f:
    # get lines from input file
    for data in f:
        # process one line
        data = process_line(data)

        # ignore empty lines or comments
        if data is None:
            continue

        # write processed line to output file
        with open(filename2,"a+") as f2:
            f2.write(f"{data}\n")