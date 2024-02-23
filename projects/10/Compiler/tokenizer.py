"""
This module will receive a JACK source code file and split it into tokens
The tokens will be stored in a file with the same filename as the source code but with xml extension
"""
import sys
import string
import os

def write_tag(
    tag : str,
    output_file : str,
    closed : bool
) -> None:
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
    with open(output_file,"a+",encoding="utf-8") as f3:
        if closed is True:
            f3.write(f"</{tag}>\n")
        else:
            f3.write(f"<{tag}>\n")

def process_input(
    c : str,
    current_state : str,
    fsa : dict[str,dict[str,str]]
) -> str:
    """
    Purpose:
        navigate to next state in FSA using input "c" which is current character

    Arguments:
        c:
            character to input into FSA (str)

        current_state:
            current state of FSA (str)

    Return:
        new state: str
    """
    # check if input "c" exists as transition in current state of FSA
    if c in fsa[current_state].keys():
        # if it does then transition to it
        current_state = fsa[current_state][c]
    else:
        # if it doesnt then get the "else" transition which captures anything else
        current_state = fsa[current_state]["else"]
    return current_state

def write_token(
    token : str,
    tag : str,
    output_file : str
):
    """
    Purpose:
        Write token to file in XML format

    Arguments:
        token:
            token to write : str

        tag:
            tag to write : str

        output_file:
            output file path : str

    Return:
        None
    """
    with open(output_file,"a+",encoding="utf-8") as f1:
        if token == "<":
            token = "&lt;"
        elif token == ">":
            token = "&gt;"
        elif token == "\"":
            token = "&quot;"
        elif token == "&":
            token = "&amp;"
        f1.write(f"<{tag}> {token} </{tag}>\n")

def handle_error(
    state : str,
    character : str,
    line_num : int,
    input_file : str
) -> None:
    """
    Purpose:
        Raise errors and exit gracefully

    Arguments:
        state:
            string that has last valid state

        character:
            character that raised the error

        line_num:
            line number

        input_file:
            file that caused the error
    Return:
        None
    """
    print(f"Error at line {line_num}: ")
    print(f"Invalid character {ord(character)}")
    print(f"final state: {state}")
    print(f"input file: {input_file}")
    sys.exit()

def process_file(
    input_file : str,
    output_file : str,
    keyword_set : set[str],
    symbols : set[str],
    fsa : dict[str,dict[str,str]]
) -> None:
    """
    Purpose:
        Process file

    Arguments:
        input_file:
            input file path

        output_file:
            output file path

        keyword_set:
            set of keywords (string)

        symbols:
            set of symbols (string)
    Return:
        None
    """
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
    with open(input_file,"a+",encoding="utf-8") as f:
        f.write("\n")

    line_num = 0

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

            if c == "\n":
                line_num += 1

            # convert character to ascii and pass it as input
            # get next state
            next_state = process_input(
                c=ord(c),
                current_state=current_state,
                fsa=fsa
            )

            # done = terminal state it is not a real state but rather a logical state
            if next_state == "done":
                # if last state was id then check
                # if dealing with keyword or identifier and write token
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
                # if current state is a symbol
                elif c in symbols:
                    # write symbol token to XML file
                    write_token(
                        token=c,
                        tag="symbol",
                        output_file=output_file
                    )
                    # reset FSA
                    current_state = "start"
                elif current_state == "symbol47":
                    # write symbol token to XML file
                    write_token(
                        token='/',
                        tag='symbol',
                        output_file=output_file
                    )
                    # go back to previous character
                    f.seek(-1,1)
                    # reset fsa
                    current_state = "start"
            elif next_state == "error":
                handle_error(
                    state=current_state,
                    character=c,
                    line_num=line_num,
                    input_file=input_file
                )
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

def generate_fsa(
    symbols : set[str]
) -> dict[str,dict[int,str]]:
    """
    Purpose:
        Generate Finite State Automata for tokenizer

    Arguments:
        symbols:
            set of strings (symbols) used by language

    Return:
        FSA which is a dictionary of form:
        {
            state:
            {
                transition: state,
                else: state
            }
        }
        The else state is used as catch all for any
        transitions not caught by the other transitions
    """
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
            ord("/"): "symbol47", # /
            13: "start", # [LR]
            10: "start", # [RF]
            ord(" "): "start", # [space]
            ord("\""): "string", # "
            ord("\t"): "start", # [\t]
            "else": "error",
        },
        # / state
        # handled differently due to comments
        "symbol47": {
            ord("/"): "slc", # /
            ord("*"): "smc", # *
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
            ord("*"): "mmc",
            "else": "smc"
        },
        # middle multiline comment
        "mmc": {
            ord("/"): "done",
            "else": "smc"
        },
        # identifier state
        "id": {
            "else": "error",
            ord("{"): "done", # {
            ord("("): "done",
            ord(","): "done",
            ord(";"): "done",
            ord("["): "done",
            ord("=") : "done",
            ord("."): "done",
            ord("+"): "done",
            ord("-"): "done",
            ord("*"): "done",
            ord("/"): "done",
            ord("&"): "done",
            ord("|"): "done",
            ord("<"): "done",
            ord(">"): "done",
            ord("]"): "done",
            ord(")"): "done",
            ord(" "): "done" # space
        },
        # integer state
        "int" : {
            ord("+"): "done",
            ord("-"): "done",
            ord("*"): "done",
            ord("/"): "done",
            ord("&"): "done",
            ord("|"): "done",
            ord(">"): "done",
            ord("<"): "done",
            ord("="): "done",
            ord("]"): "done",
            ord(";"): "done",
            ord(")"): "done",
            ord(","): "done",
            "else": "error"
        },
        # string state
        "string": {
            "else": "string",
            ord("\""): "done", # "
            ord("\\"): "escape" # \
        },
        # escape state
        "escape": {
            "else": "string"
        }
    }

    # create set of valid characters (a-z,A-Z,_)
    valid_chars = set(string.ascii_letters).union(set({'_'}))

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
        if ord(v) not in fsa["start"]:
            # map start to symbol in format symbol(symbol ascii code) via symbol ascii code
            fsa["start"][ord(v)] = "done"

    return fsa

def main():
    """
    Purpose:
        Entry point of program

    Arguments:
        None

    Return:
        None
    """
    # get cmd args
    n = len(sys.argv)

    try:
        assert n == 2
    except AssertionError:
        print("Error: Missing or too many arguments")
        print("Program should be run: ")
        print("<program name> <source code>")
        sys.exit()
    # get filename
    filename = sys.argv[1]

    # set of symbols
    symbols = set({
        '{','}','(',')','[',']','.',
        ',',';','+','-','*','/','&',
        '|','<','>','=','~'
    })

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

    fsa = generate_fsa(symbols=symbols)

    # check if directory
    if os.path.isdir(filename):
        # get directory name
        dir_name = sys.argv[1]

        # iterate over files
        for file in os.listdir(dir_name):
            # get file
            if file.endswith(".jack"):
                output_file_name = file.split('/')[-1].split('.')[0]
                output_file_name = f"{output_file_name}T1.xml"
                input_file = f"{filename}/{file}"
                process_file(
                    input_file=input_file,
                    output_file=output_file_name,
                    keyword_set=keyword_set,
                    symbols=symbols,
                    fsa=fsa
                )
    else:
        # get single filename
        input_file = sys.argv[1]
        # get filename without extension
        filename = input_file.split('/')[-1].split('.')[0]
        # output file name
        output_file_name = f"{filename}T1.xml"
        process_file(
            input_file=input_file,
            output_file=output_file_name,
            keyword_set=keyword_set,
            symbols=symbols,
            fsa=fsa
        )

if __name__ == "__main__":
    main()
