import sys

# get cmd args
n = len(sys.argv)

if n < 0:
    raise Exception("Missing arguments. pass filename.asm as argument")

if n > 2:
    raise Exception("Too many arguments")

# get filename
filename = sys.argv[1]

# symbol table and constants

symbol_table = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "SCREEN": 16384,
    "KBD": 24576
}

jump_table = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

dest_table = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

comp_table_0 = {
    "0": "101010",
    "1": "111111",
    "-1": "111010",
    "D": "001100",
    "A": "110000",
    "!D": "001101",
    "!A": "110001",
    "-D": "011111",
    "-A": "110011",
    "D+1": "011111",
    "A+1": "110111",
    "D-1": "001110",
    "A-1": "110010",
    "D+A": "000010",
    "D-A": "010011",
    "A-D": "000111",
    "D&A": "000000",
    "D|A": "010101"
}

comp_table_1 = {
    "M": "110000",
    "!M": "110001",
    "M+1": "110111",
    "M-1": "110010",
    "D+M": "000010",
    "D-M": "010011",
    "M-D": "000111",
    "D&M": "000000",
    "D|M": "010101"
}

for i in range(0,16):
    symbol_table[f"R{i}"] = i

"""
Purpose:
    Encode A-instruction to binary

Arguments:
    label:
        decimal value to encode

Return:
    ins:
        binary string of encoded values
"""
def encode_A_ins(label):
    # A-instruction start with 0
    ins = "0"

    label = int(label)

    # convert dec to binary
    label = bin(label).replace("0b","")
    # 16-bit instruction -1 for opcode leaves 15 bit for values
    # calculate how many leading 0's to pad
    n = 15 - len(label)
    # pad with leading 0's
    for _ in range(n):
        ins += "0"
    # add binary instruction
    for l in label:
        ins += l
    return ins

"""
Purpose:
    encode computation bits

Arguments:
    data:
        string that contains comp instruction in C-instruction

Return:
    comp_bits:
        computation instruction encoded in binary
"""
def encode_comp_bits(data):
    # M = a = 1
    if "M" in data:
        comp_bits = f"1{comp_table_1[data]}"
    else:
        comp_bits = f"0{comp_table_0[data]}"
    return comp_bits

"""
Purpose:
    Encode destination bits

Arguments:
    data:
        string that contains C-instruction

Return:
    ins:
        binary string that encodes computation bits and destination bits
"""
def encode_dest_comp_bits(data):
    # data is in format:
    # dest = comp
    # split destination and computation
    data = data[0].split("=")

    # check if dest bits are set
    if len(data) == 2:
        #dest is set
        # data[0] = dest
        dest_bits = dest_table[data[0]]
        
        # data[1] = comp
        comp_bits = encode_comp_bits(data[1])
    else:
        # dest is not set 
        dest_bits = dest_table["null"]

        # data[0] = comp 
        comp_bits = encode_comp_bits(data[0])

    # encode computation and destination bits
    ins = f"{comp_bits}{dest_bits}"

    return ins

"""
Purpose:
    Encode C-instruction

Arguments:
    data:
        string that contains C-instruction

Return:
    ins:
        binary string that encodes the C-instruction
"""
def encode_C_ins(data):
    # C-instruction
    # get JMP instruction
    data = data.split(';')

    # JMP instruction found
    if len(data) == 2:
        # encode jump instruction bits
        jump_bits = jump_table[data[1]]
    else:
        # no jump instruction
        # encode jump bits
        jump_bits = jump_table["null"]

    # encode destination and computation bits
    dest_comp_bits = encode_dest_comp_bits(data)

    # encode C-ins
    ins = f"111{dest_comp_bits}{jump_bits}"

    return ins

"""
Purpose:
    get assembly instruction

Arguments:
    data:
        string that contains file line

Return:
    None if data is white line or comment
    Otherwise it will return an assembly instruction
"""
def get_assembly_instruction(data):
    # skip white lines
    if len(data) == 1:
        return None
    
    # remove white space
    data = data.replace(" ","")

    data = data.replace("\n","")

    # remove comments
    data = data.split("//")
    data = data[0]

    # remove lines that start with comments
    if len(data) == 0:
        return None

    return data

"""
Purpose:
    Get loop labels

Arguments:
    data:
        string that contains assembly instruction

    x:
        program counter

Return:
    x:
        updated program counter
"""
def get_loop_labels(data,x):
    # check if loop label
    if data[0] == "(":
        # get label
        label = data[1:len(data)-1]
        # add label to symbol table if not exists
        if label not in symbol_table:
            symbol_table[label]=x+1
    # increment program counter
    else:
        x = x + 1

    return x

"""
Purpose:
    Get variables from assembly program

Arguments:
    data:
        assembly instruction

    label_count:
        variable counter (used to allocate memory)

Return:
    label_count:
        updated variable counter
"""
def get_variables(data,label_count):
    # process only A-instructions
    if data[0] == "@":
        # get label or hard-coded address
        label = data[1:]
        # if label starts with a digit then it is a hardcoded address so you can encode directly
        if label[0].isdigit() == False:
            # if label doesn't start with digit then it is a variable
            # if variable is not in symbol table then add it
            if label not in symbol_table:
                symbol_table[label]=label_count
                label_count += 1

    return label_count

"""
Purpose:
    Get binary instructions

Arguments:
    data:
        string that contains assembly instruction

Return:
    None if label for loop
    Otherwise it will return the bit encoded instruction
"""
def get_instructions(data):
    # skip labels for loops because they have already been processed
    if data[0] == "(":
        return None
    
    # check if dealing with A-instruction
    if data[0] == "@":
        # get label or hard-coded address
        label = data[1:]
        # if label starts with a digit then it is a hardcoded address so you can encode directly
        if label[0].isdigit():
            ins = encode_A_ins(label)
        else:
            # if label doesn't start with digit then it is a variable
            # if variable is not in symbol table then add it
            if label in symbol_table:
                # if variable is in symbol table then encode the instruction
                ins = encode_A_ins(symbol_table[label])
    else:
        # encode C-instruction
        ins = encode_C_ins(data)

    return ins

x = -1
label_count = 16

for pass_count in range(3):
    with open(filename,"r") as f:
        for data in f:
            # get assembly instruction from file
            data = get_assembly_instruction(data)
            
            # skip if is not assembly instruction
            if data is None:
                continue

            # different processing for passes
            if pass_count == 0:
                # first pass gets loop labels
                x = get_loop_labels(data,x)
            elif pass_count == 1:
                # second pass gets all variables
                label_count = get_variables(data,label_count)
            else:
                # 3rd pass converts all assembly instructions
                ins = get_instructions(data)

                if ins is not None:
                    filename2 = f"{filename[0:len(filename)-4]}.hack2"
                    with open(filename2,"a+") as f2:
                        f2.write(f"{ins}\n")