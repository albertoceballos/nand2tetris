import sys
import string
import os

# get cmd args
n = len(sys.argv)

# missing filename
if n < 2:
    raise Exception("Missing arguments. pass filename")

# too many args
if n > 2:
    raise Exception("Too many arguments")

# Finite State Automata
# described by picture "finite_state_automata_tokenizer" in folder
# uses ASCII values for characters
# LR, RF = \n
# in image:
#   L = {a-zA-Z}
#   D = {0-9}
#   S = {set of symbols}
fsa = {
    "start":{
        47: "symbol47", # /
        13: "start", # [LR]
        10: "start", # [RF]
        32: "start", # [space]
        34: "string", # "
        "else": "start",
    },
    # / state
    # handled differently due to comments
    "symbol47": {
        47: "slc", # /
        42: "smc", # *
        "else": "done"
    },
    # start line comment
    "slc": {
        10: "done", # LF
        13: "done", # CR
        "else": "slc"
    },
    # start multline comment
    "smc": {
        42: "mmc",
        "else": "smc"
    },
    # middle multiline comment
    "mmc": {
        47: "done",
        "else": "smc"
    },
    # identifier state
    "id": {
        "else": "done"
    },
    # integer state
    "int" : {
        "else": "done"
    },
    # string state
    "string": {
        "else": "string",
        34: "done", # "
        92: "escape" # \
    },
    # escape state
    "escape": {
        "else": "string"
    }
}

# create set of valid characters (a-z,A-Z,_)
valid_chars = set(string.ascii_letters).union(set({'_'}))

# set of symbols
symbols = set({
    '{','}','(',')','[',']','.',
    ',',';','+','-','*','/','&',
    '|','<','>','=','~'
})

# convert symbols in symbol set to symbol(symbol ascii code)
symbols_name = set()

# set of keywords
keyword_set = set({
    'class',
    'constructor',
    'function',
    'method',
    'field',
    'static',
    'var',
    'int',
    'char',
    'boolean',
    'void',
    'true',
    'false',
    'null',
    'this',
    'let',
    'do',
    'if',
    'else',
    'while',
    'return'
})

# map transition from start state to identifier state via a-z,A-Z,_
# also map transition from identifier to identifier state via a-z,A-Z,_
for v in valid_chars:
    fsa["start"][ord(v)] = "id"
    fsa["id"][ord(v)] = "id"

# map identifier to identifier via 0-9
# also map start to int via 0-9
# also map int to int via 0-9
for v in range(0,10):
    fsa["id"][ord(str(v))] = "id"
    fsa["start"][ord(str(v))] = "int"
    fsa["int"][ord(str(v))] = "int"

for v in symbols:
    # avoid /
    if ord(v) not in fsa["start"].keys():
        # map start to symbol in format symbol(symbol ascii code) via symbol ascii code
        fsa["start"][ord(v)] = f"symbol{ord(v)}"

    # create symbol(symbol ascii code) entry and map it to done via all characters
    if f"symbol{ord(v)}" not in fsa.keys():
        fsa[f"symbol{ord(v)}"] = {
            "else": "done"
        }

    # create set of symbol (symbol ascii code) used for terminal state determination
    symbols_name.add(f"symbol{ord(v)}")

"""
Purpose:
    write opening and closing tag for set of statements

Arguments:
    tag:
        tag to write

    output_file:
        output file

    closed:
        flag to determine if write closed tag or open tag

Return:
    None
"""
def write_tag(tag,output_file,closed):
    with open(output_file,"a+") as f3:
        if closed is True:
            f3.write(f"</{tag}>\n")
        else:
            f3.write(f"<{tag}>\n")

"""
Purpose:
    navigate to next state in FSA using input "c" which is current character

Arguments:
    c:
        character to input into FSA

    current_state:
        current state of FSA

Return:
    new state
"""
def process_input(c,current_state):
    # check if input "c" exists as transition in current state of FSA
    if c in fsa[current_state].keys():
        # if it does then transition to it
        current_state = fsa[current_state][c]
    else:
        # if it doesnt then get the "else" transition which captures anything else
        current_state = fsa[current_state]["else"]
    return current_state

"""
Purpose:
    Write token to file in XML format

Arguments:
    token:
        token to write

    tag:
        tag to write

    output_file:
        output file path

Return:
    None
"""
def write_token(token, tag,output_file):
    with open(output_file,"a+") as f1:
        f1.write(f"<{tag}> {token} </{tag}>\n")

"""
Purpose:
    Process file

Arguments:
    input_file:
        input file path

    output_file:
        output file path

Return:
    None
"""
def process_file(input_file,output_file):
    # current state flag
    current_state = "start"
    # identifier name (used to determine variable names, keywords, symbols)
    id_name = ""
    # write <tokens> to file (opening XML tag for file)
    write_tag(
        tag="tokens",
        output_file=output_file,
        closed=False
    )
    # add \n to input_file to bypass last token issue at EOF
    with open(input_file,"a+") as f:
        f.write("\n")

    # read file in binary to be able to seek previous character
    with open(input_file,"rb") as f:
        # loop until done
        while True:
            # read data as binary and decode as utf-8
            c = f.read(1).decode("utf-8")
            # check if EOF
            if not c:
                print("end of file")
                break

            # convert character to ascii and pass it as input
            # get next state
            next_state = process_input(ord(c),current_state)

            # done = terminal state it is not a real state but rather a logical state
            if next_state == "done":
                # if last state was id then check if dealing with keyword or identifier and write token
                if current_state == "id":
                    if id_name in keyword_set:
                        write_token(
                            token=id_name,
                            tag="keyword",
                            output_file=output_file
                        )
                    else:
                        write_token(
                            token=id_name,
                            tag="identifier",
                            output_file=output_file
                        )
                    # reset id_name
                    id_name = ""
                    # reset FSA
                    current_state = "start"
                    # move cursor to prev character
                    f.seek(-1,1)
                # if current state is a symbol
                elif current_state in symbols_name:
                    # get symbol
                    symbol = chr(int(current_state.split("symbol")[1]))
                    # write symbol token to XML file
                    write_token(
                        token=symbol,
                        tag="symbol",
                        output_file=output_file
                    )
                    # move cursor to previous character
                    f.seek(-1,1)
                    # reset FSA
                    current_state = "start"
                # if dealing with comment
                elif current_state == "mmc" or current_state == "slc":
                    current_state = "start"
                # if dealing with int
                elif current_state == "int":
                    # write integer constant token
                    write_token(
                        token=id_name,
                        tag="integerConstant",
                        output_file=output_file
                    )
                    # seek prev character
                    f.seek(-1,1)
                    # reset id_name and FSA state
                    id_name = ""
                    current_state = "start"
                # if dealing with string
                elif current_state == "string":
                    # write string constant token
                    write_token(
                        token=id_name,
                        tag="stringConstant",
                        output_file=output_file
                    )
                    # reset id_name and FSA state
                    id_name = ""
                    current_state = "start"
            else:
                # not final state
                # set id_name value
                if current_state == "id" or next_state == "id" or \
                current_state == "int" or next_state == "int" or \
                current_state == "string" or next_state == "string":
                    # bypass bug where it keeps last " in string
                    if c != "\"":
                        id_name += c
                # set current state to next state
                current_state = next_state
        # write </tokens> to XML file
        write_tag(
            tag="tokens",
            output_file=output_file,
            closed=True
        )

# get filename
filename = sys.argv[1]

# check if directory
if os.path.isdir(filename):
    # get directory name
    dir_name = sys.argv[1]

    # get output file name
    output_file_name = f"{dir_name}/{dir_name.split('/')[-1]}T.xml"

    # iterate over files
    for file in os.listdir(dir_name):
        # get file
        if file.endswith(".jack"):
            input_file = f"{filename}/{file}"
            process_file(
                input_file=input_file,
                output_file=output_file_name
            )
else:
    # get single filename
    input_file = sys.argv[1]
    # get filename without extension
    filename = input_file.split('/')[-1].split('.')[0]
    # output file name
    output_file_name = f"{filename}T.xml"
    process_file(
        input_file=input_file,
        output_file=output_file_name
    )