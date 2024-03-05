"""
This module will parse an XML file that contains tokens
and will add the context of class, procedures, variables, and so on
This is based on the nand2tetris book
"""
import sys
import os
import xml.etree.ElementTree as ET
from jack_code_gen import add_to_symbol_table, reset_symbol_table, \
    write_arithmetic_op, write_label, \
    write_function_call, \
    write_push_pop, get_label, \
    get_symbol_from_table, get_class_name, set_class_name

output_file = ""
current_index = -1
input_file = ""
token_list = []
token = dict()

def write_tag(
    tag,
    is_closed
):
    """
    Purpose:
        write opening or closing tag

    Argument:
        tag : str
            tag to write

        is_closed : bool
            boolean flag to determine if write closed tag or open tag

    Return:
        None
    """
    global output_file
    try:
        assert isinstance(output_file,str)
        assert isinstance(tag,str)
        assert isinstance(is_closed,bool)
        with open(output_file,"a+",encoding="utf-8") as f:
            if is_closed is True:
                f.write(f"</{tag}>\n")
            else:
                f.write(f"<{tag}>\n")
    except AssertionError:
        print("Invalid arguments")
        print(f"output_file = {output_file}")
        print(f"tag = {tag}")
        print(f"is_closed = {is_closed}")
        sys.exit()

def write_token():
    """
    Purpose:
        write value enclosed between tags

    Arguments:
        None

    Return:
        None
    """
    global output_file, token
    try:
        assert isinstance(output_file,str)
        assert isinstance(token,dict)
        assert 'tag' in token and 'value' in token
        # encode these tags because they
        # cause an issue with parsing
        if token['value'] == "<":
            token['value'] = "&lt;"
        elif token['value'] == ">":
            token['value'] = "&gt;"
        elif token['value'] == "\"":
            token['value'] = "&quot;"
        elif token['value'] == "&":
            token['value'] = "&amp;"
        with open(output_file,"a+",encoding="utf-8") as f:
            f.write(f"<{token['tag']}>{token['value']}</{token['tag']}>\n")
    except AssertionError:
        print("Error: ")
        print("Invalid arguments")
        print(f"token = {token}")
        print(f"output_file = {output_file}")
        sys.exit()

def verify_token_type(expected_tokens):
    """
    Purpose:
        verify that token matches expected value

    Argument:
        expected_token : list
            list token to compare to where each entry is of form
            dictionary of type{
                tag: string,
                value: string
            }

    Return:
        None
    """
    global input_file, token
    try:
        assert isinstance(input_file,str)
        assert isinstance(token,dict)
        assert 'tag' in token
        assert isinstance(expected_tokens,list)

        valid = False
        for e in expected_tokens:
            assert isinstance(e,dict)
            assert 'tag' in e
            if 'value' in e.keys():
                valid = (token['tag'] == e['tag'] and token['value'] == e['value'])
            else:
                valid = token['tag'] == e['tag']

            if valid:
                break

        assert valid is True
    except AssertionError:
        print("Error: Invalid token")
        print(f"File: {input_file}")
        print(f"Received tag: {token['tag']}")
        print(f"Received value: {token['value']}")

        c = 0
        for e in expected_tokens:
            print(f"Expected tag: {e['tag']}")
            if 'value' in e.keys():
                print(f"with Expected value: {e['value']}")
            if c + 1 < len(expected_tokens):
                print("OR")
            c += 1
        sys.exit()

def process_class():
    """
    Purpose:
        process class

    Arguments:
        None

    Return:
        None
    """
    global current_index, token
    try:
        assert isinstance(current_index,int)
        assert isinstance(token,dict)
        assert 'tag' in token and 'value' in token

        # reset class symbol table
        reset_symbol_table(is_class_level=True)
        # write <class> tag
        write_tag(tag="class",is_closed=False)

        # verify if tag is class else raise Exception
        verify_token_type(
            expected_tokens=[{'tag':'keyword','value':'class'}]
        )

        # write <keyword> class </keyword> token
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

        # verify if tag is class else raise Exception
        verify_token_type(expected_tokens=[{'tag':'identifier'}])

        set_class_name(token['value'].replace(" ",""))

        # write <identifer> className </identifier> token
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

        # verify if tag is class else raise Exception
        verify_token_type(expected_tokens=[{'tag':'symbol','value':'{'}])

        # write <symbol> { </symbol> token
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

        # 0 or more class var declarations
        while token['tag'] == "keyword" and (token['value'] == "static" or token["value"] == "field"):
            # process variable declaration
            process_class_var_declaration()

        # 0 or more subroutine declarations
        while token['tag'] == "keyword" and \
        (token['value'] == "constructor" or token['value'] == "function" or \
        token['value'] == "method"):
            # process subroutine declaration
            process_subroutine_declaration()

        # verify if tag is class else raise Exception
        verify_token_type(expected_tokens=[{'tag':'symbol','value':'}'}])

        # write <symbol> } </symbol> token
        write_token()

        # write </class>
        write_tag(tag="class",is_closed=True)
    except AssertionError:
        print("Error: invalid arguments")
        print(f"current_index = {current_index}")
        print(f"token = {token}")
        sys.exit()

def process_subroutine_declaration():
    """
    Purpose:
        process subroutine declaration

    Arguments:
        None

    Return:
        None
    """
    global token, current_index
    verify_token_and_current_index()

    # write <subroutineDec>
    write_tag(tag="subroutineDec",is_closed=False)

    reset_symbol_table(is_class_level=False)

    verify_token_type(
        expected_tokens=[
            {'tag': 'keyword', 'value': 'constructor'},
            {'tag': 'keyword', 'value': 'function'},
            {'tag': 'keyword', 'value': 'method'}
        ]
    )

    sub_type = token['value'].replace(" ","")

    class_name = get_class_name()

    if token['tag'] == 'keyword' and sub_type == 'method':
        add_to_symbol_table(
            name="this",
            id_type=class_name,
            kind="argument",
            var_classification="object",
            is_class_level=False
        )

    # write <keyword> constructor OR function OR method </keyword>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    verify_token_type(
        expected_tokens=[
            {'tag':'keyword','value':'void'},
            {'tag':'keyword','value':'int'},
            {'tag':'keyword','value':'char'},
            {'tag':'keyword','value':'boolean'},
            {'tag':'identifier'},
        ]
    )

    # write <keyword> void OR int OR char OR boolean </keyword>
    # OR <identifier> className </identifier>
    write_token()

    id_type = token['value'].replace(" ","")

    # get next token
    current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'identifier'}])

    # write <identifier> subprocedure name </identifier>
    write_token()

    sub_name = token['value'].replace(" ","")

    var_classification = "method" if sub_type in ("constructor","method") else "function"

    add_to_symbol_table(
        name=sub_name,
        id_type=id_type,
        kind="none",
        var_classification=var_classification,
        is_class_level=True
    )

    # get next token
    current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'symbol','value':'('}])

    # write <symbol> ( </symbol>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    process_parameter_list()

    verify_token_type(expected_tokens=[{'tag':'symbol','value':')'}])

    # write <symbol> ) </symbol>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    process_subroutine_body()

    # write </subroutineDec>
    write_tag(tag="subroutineDec",is_closed=True)

def process_subroutine_body():
    """
    Purpose:
        process subroutine body
    Arguments:
        None
    Return:
        None
    """
    global token, current_index

    verify_token_and_current_index()
    # write <subroutineBody>
    write_tag(tag="subroutineBody",is_closed=False)

    verify_token_type(expected_tokens=[{'tag':'symbol','value':'{'}])

    # write <symbol> { </symbol>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    while token['tag'] == 'keyword' and token['value'] == 'var':
        process_variable_declaration()

    process_statements()

    verify_token_type(expected_tokens=[{'tag':'symbol','value':'}'}])

    # write <symbol> } </symbol>
    write_token()

    current_index, token = get_next_token(i=current_index)

    # write </subroutineBody>
    write_tag(tag="subroutineBody",is_closed=True)

def process_statements():
    """
    Purpose:
        process statements
    Arguments:
        None
    Return:
        None
    """
    global token, current_index

    verify_token_and_current_index()
    # write <statements>
    write_tag(tag="statements",is_closed=False)

    while token['tag'] == 'keyword' and \
        (token['value'] == 'let' or token['value'] == 'if' or \
        token['value'] == 'while' or token['value'] == 'do' or \
        token['value'] == 'return'):
        if token['tag'] == 'keyword' and token['value'] == 'let':
            process_let_statement()
        elif token['tag'] == 'keyword' and token['value'] == 'if':
            process_if_statement()
        elif token['tag'] == 'keyword' and token['value'] == 'while':
            process_while_statement()
        elif token['tag'] == 'keyword' and token['value'] == 'do':
            process_do_statement()
        elif token['tag'] == 'keyword' and token['value'] == 'return':
            process_return_statement()

    # write </statements>
    write_tag(tag="statements",is_closed=True)

def process_while_statement():
    """
    Purpose:
        process while statements

    Arguments:
        None

    Return:
        None
    """
    global token, current_index
    verify_token_and_current_index()
    # write <whileStatement>
    write_tag(tag="whileStatement",is_closed=False)

    verify_token_type(expected_tokens=[{'tag':'keyword','value':'while'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'symbol','value':'('}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    l1 = get_label()
    l2 = get_label()

    # write label L1
    write_label(label_type="label",label_id=l1)

    # process expression
    process_expression()

    verify_token_type(expected_tokens=[{'tag':'symbol','value':')'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'symbol','value':'{'}])

    write_token()

    # write not
    write_arithmetic_op(op="not")

    # write if-goto L2
    write_label(label_type="if-goto",label_id=l2)

    current_index, token = get_next_token(i=current_index)

    # process statements
    process_statements()

    verify_token_type(expected_tokens=[{'tag':'symbol','value':'}'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    write_label(label_type="goto",label_id=l1)

    write_label(label_type="label",label_id=l2)

    # write </whileStatement>
    write_tag(tag="whileStatement",is_closed=True)

def process_if_statement():
    """
    Purpose:
        process if statements

    Arguments:
        None   
    Return:
        None
    """
    global current_index, token
    verify_token_and_current_index()

    # write <ifStatement>
    write_tag(tag="ifStatement",is_closed=False)

    verify_token_type(expected_tokens=[{'tag':'keyword','value':'if'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'symbol','value':'('}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    # process expression inside if statement
    # and generate code for expression
    process_expression()

    verify_token_type(expected_tokens=[{'tag':'symbol','value':')'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'symbol','value':'{'}])

    # negate expression
    write_arithmetic_op(op="neg")

    # get labels
    label_n = get_label()

    # write label N
    write_label(label_type="if-goto",label_id=label_n)

    write_token()

    current_index, token = get_next_token(i=current_index)

    # write s1
    process_statements()
    
    verify_token_type(expected_tokens=[{'tag':'symbol','value':'}'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    if token['tag'] == 'keyword' and token['value'] == 'else':
        label_y = get_label()
        write_label(label_type="goto",label_id=label_y)

        write_label(label_type="label",label_id=label_n)

        write_token()

        current_index, token = get_next_token(i=current_index)
        
        verify_token_type(expected_tokens=[{'tag':'symbol','value':'{'}])

        write_token()

        current_index, token = get_next_token(i=current_index)
        # write s2
        process_statements()

        verify_token_type(expected_tokens=[{'tag':'symbol','value':'}'}])

        write_token()

        current_index, token = get_next_token(i=current_index)

        write_label(label_type="label",label_id=label_y)
    else:
        write_label(label_type="label",label_id=label_n)

    # write </ifStatement>
    write_tag(tag="ifStatement",is_closed=True)

def process_do_statement():
    """
    Purpose:
        process do statements

    Arguments:
        None

    Return:
        None
    """
    global current_index, token

    verify_token_and_current_index()

    # write <doStatement>
    write_tag(tag="doStatement",is_closed=False)

    verify_token_type(expected_tokens=[{'tag':'keyword','value':'do'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    process_subroutine_call()

    verify_token_type(expected_tokens=[{'tag':'symbol','value':';'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    # write </doStatement>
    write_tag(tag="doStatement",is_closed=True)

def verify_token_and_current_index():
    """
    Purpose:
        ensure that token has valid data type and keys
        ensure that index is valid

    Arguments:
        None

    Return:
        None
    """
    global token, current_index
    try:
        assert isinstance(token,dict)
        assert 'tag' in token and 'value' in token
        assert isinstance(current_index,int)
    except AssertionError:
        print("Error: invalid arguments")
        print(f"current_index = {current_index}")
        print(f"token = {token}")
        sys.exit()

def process_return_statement():
    """
    Purpose:
        process return statements
    Arguments:
        None
    Return:
        None
    """
    global token, current_index
    verify_token_and_current_index()
    # write <returnStatement>
    write_tag(tag="returnStatement",is_closed=False)

    verify_token_type(expected_tokens=[{'tag':'keyword','value':'return'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    if token['tag'] == 'integerConstant' or \
    token['tag'] == 'stringConstant' or \
    token['tag'] == 'keyword' and \
    (token['value'] == 'true' or token['value'] == 'false' or \
    token['value'] == 'null' or token['value'] == 'this') or \
    token['tag'] == 'identifier' or \
    token['tag'] == 'symbol' and (token['value'] == '-' or token['value'] == '~') or \
    token['tag'] == 'symbol' and token['value'] == '(':
        current_index, token = process_expression()

    verify_token_type(expected_tokens=[{'tag':'symbol','value':';'}])

    write_token()

    current_index, token = get_next_token(i=current_index)

    # write </returnStatement>
    write_tag(tag="returnStatement",is_closed=True)

def process_let_statement():
    """
    Purpose:
        process let statements

    Arguments:
        None

    Return:
        None
    """
    global current_index, token
    verify_token_and_current_index()
    # write <letStatement>
    write_tag(tag="letStatement",is_closed=False)

    verify_token_type(expected_tokens=[{'tag':'keyword','value':'let'}])

    # write <keyword> let </keyword> token
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'identifier'}])

    var = get_symbol_from_table(name=token['value'].replace(" ",""))

    seg = "this" if var['kind'] == 'field' else var['kind']

    write_push_pop(segment=seg,index=var['num'],is_push=False)

    # write <identifier> varName </identifier>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    if token['tag'] == 'symbol' and token['value'] == '[':
        # write <symbol> [ </symbol>
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

        process_expression()

        verify_token_type(expected_tokens=[{'tag':'symbol','value':']'}])

        # write <symbol> ] </symbol>
        write_token()

        current_index, token = get_next_token(i=current_index)


    verify_token_type(expected_tokens=[{'tag':'symbol','value':'='}])

    # write <symbol> = </symbol>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    process_expression()

    verify_token_type(expected_tokens=[{'tag':'symbol','value':';'}])

    # write <symbol> ; </symbol>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    # write </letStatement>
    write_tag(tag="letStatement",is_closed=True)

def process_expression():
    """
    Purpose:
        process expression

    Arguments:
        None

    Return:
        None
    """
    global token, current_index
    verify_token_and_current_index()
    # write <expression>
    write_tag(tag="expression",is_closed=False)

    #print(f"process expression received = {token}")

    process_term()

    while token['tag'] == 'symbol' and \
        (token['value'] == '+' or token['value'] == '-' or \
        token['value'] == '*' or token['value'] == '/' or \
        token['value'] == '&' or token['value'] == '|' or \
        token['value'] == '<' or token['value'] == '>' or \
        token['value'] == '='):
        op = token['value'].replace(" ","")

        # write operator
        write_token()

        current_index, token = get_next_token(i=current_index)

        # process term
        process_term()

        if op == '*':
            write_function_call(function_name="Math.multiply",num_args=2)
        elif op == "/":
            write_function_call(function_name="Math.divide",num_args=2)
        else:
            write_arithmetic_op(op=op)
    
    # write </expression>
    write_tag(tag="expression",is_closed=True)

    return current_index, token

def process_term():
    """
    Purpose:
        process term
    Arguments:
        None
    Return:
        None
    """
    global current_index, token
    verify_token_and_current_index()
    # write <term>
    #print(f"process term received token={token}")

    write_tag(tag="term",is_closed=False)

    if token['tag'] == 'integerConstant':
        # write <integerConstant> int constant </integerConstant>
        write_token()

        current_index, token = get_next_token(i=current_index)

        # write push const n
        write_push_pop(segment="const",index=token,is_push=True)
    elif token['tag'] == 'stringConstant':
        # write <stringConstant> string constant </stringConstant>
        write_token()

        current_index, token = get_next_token(i=current_index)

        s = token['value'].replace(" ","")

        write_push_pop(segment="constant",index=len(s),is_push=True)
        
        write_function_call("String.new",1)

        for ch in s:
            write_push_pop(segment="constant",index=ord(ch),is_push=True)
            write_function_call(function_name="String.appendChar",num_args=2)

    elif token['tag'] == 'keyword' and \
        (token['value'] == 'true' or token['value'] == 'false' or\
        token['value'] == 'null' or token['value'] == 'this'):
        # write <keyword> true OR false OR null OR this </keyword>
        write_token()

        if token['value'] == 'this':
            write_push_pop(segment="pointer",index=0,is_push=True)
        else:
            write_push_pop(segment="constant",index=0,is_push=True)

            if token['value'] == "true":
                write_arithmetic_op(op="not")

        current_index, token = get_next_token(i=current_index)
    elif token['tag'] == 'identifier':
        next_index, next_token = get_next_token(i=current_index)

        if next_token['tag'] == 'symbol' and next_token['value'] == '[':
            # write <identifier> var name </identifier>
            write_token()

            array_var = token['value'].replace(" ","")
            array_var = get_symbol_from_table(name=array_var)

            token=next_token
            current_index=next_index

            verify_token_type(expected_tokens=[{'tag':'symbol','value':'['}])

            # write <symbol> [ </symbol>
            write_token()

            current_index, token = get_next_token(i=current_index)

            process_expression()

            verify_token_type(expected_tokens=[{'tag':'symbol','value':']'}])

            # write <symbol> ] </symbol>
            write_token()

            current_index, token = get_next_token(i=current_index)

            write_push_pop(segment=array_var['kind'],index=array_var['num'],is_push=True)
            write_arithmetic_op(op="add")
            write_push_pop(segment="pointer",index=1,is_push=False)
            write_push_pop(segment="that",index=0,is_push=True)
        elif next_token['tag'] == 'symbol' and (next_token['value'] == '(' or next_token['value'] == '.'):
            process_subroutine_call()
        else:
            # write <identifier> var name </identifier>
            write_token()

            variable = get_symbol_from_table(name=token['value'].replace(" ",""))

            seg = 'this' if variable['kind'] == 'field' else variable['kind']

            write_push_pop(segment=seg,index=variable['num'],is_push=True)

            token=next_token
            current_index=next_index
    # check if dealing with unaryOp (- or ~)
    elif token['tag'] == 'symbol' and (token['value'] == '-' or token['value'] == '~'):
        # write <symbol> ~ OR - </symbol>
        write_token()

        current_index, token = get_next_token(i=current_index)

        process_term()

        if token['value'] == '-':
            write_arithmetic_op(op="neg")
        else:
            write_arithmetic_op(op="not")
    
    elif token['tag'] == 'symbol' and token['value'] == '(':
        # write <symbol> ( </symbol>
        write_token()

        current_index, token = get_next_token(i=current_index)

        process_expression()

        verify_token_type(expected_tokens=[{'tag':'symbol','value':')'}])

        # write <symbol> ) </symbol>
        write_token()

        current_index, token = get_next_token(i=current_index)

    # write </term>
    write_tag(tag="term",is_closed=True)

def process_subroutine_call():
    """
    Purpose:
        process subroutine call

    Arguments:
        None

    Return:
        None
    """
    global current_index, token
    verify_token_and_current_index()
    
    verify_token_type(expected_tokens=[{'tag':'identifier'}])
    # write <identifier> subroutine name or class name or var name </identifier>
    write_token()

    proc_name = token['value'].replace(" ","")
    proc_var = get_symbol_from_table(name=proc_name)

    # get next token
    current_index, token = get_next_token(i=current_index)

    if token['tag'] == 'symbol' and token['value'] == '(':
        class_name = get_class_name()
        fun_name = f"{class_name}.{proc_name}"
        write_push_pop(segment="pointer",index=0,is_push=True)
        # write <symbol> ( </symbol>
        write_token()

        current_index, token = get_next_token(i=current_index)

        #print(f"token = {token}")

        num_args = process_expression_list()

        num_args += 1

        verify_token_type(expected_tokens=[{'tag':'symbol','value':')'}])

        # write <symbol> ) </symbol>
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)
    
        write_function_call(function_name=fun_name,num_args=num_args)
    elif token['tag'] == 'symbol' and token['value'] == '.':
        # write <symbol> . </symbol>
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

        verify_token_type(expected_tokens=[{'tag':'identifier'}])

        subproc_name = token['value'].replace(" ","")

        if proc_var['var_classification'] == 'class':
            fun_name = f"{proc_name}.{subproc_name}"
        elif proc_var['var_classification'] == 'object':
            fun_name = f"{proc_var['id_type']}.{subproc_name}"
            kind = "this" if proc_var['kind'] == 'field' else proc_var['kind']
            write_push_pop(segment=kind,index=proc_var['num'],is_push=True)

        # write <identifier> subroutine name </identifier>
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

        verify_token_type(expected_tokens=[{'tag':'symbol','value':'('}])

        # write <symbol> ( </symbol>
        write_token()

        current_index, token = get_next_token(i=current_index)

        num_args = process_expression_list()

        num_args += 1

        verify_token_type(expected_tokens=[{'tag':'symbol','value':')'}])

        # write <symbol> ) </symbol>
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)
        write_function_call(function_name=fun_name,num_args=num_args)

def process_expression_list():
    """
    Purpose:
        process subroutine call

    Arguments:
        None

    Return:
        num_args : int
            number of arguments counted in expression list
    """
    global current_index, token
    verify_token_and_current_index()

    # write <expressionList>
    write_tag(tag="expressionList",is_closed=False)

    should_run = False

    num_args = 0

    if token['tag'] == 'integerConstant' or \
    token['tag'] == 'stringConstant' or \
    token['tag'] == 'keyword' and \
    (token['value'] == 'true' or token['value'] == 'false' or \
    token['value'] == 'null' or token['value'] == 'this') or \
    token['tag'] == 'identifier' or \
    token['tag'] == 'symbol' and (token['value'] == '-' or token['value'] == '~') or \
    token['tag'] == 'symbol' and token['value'] == '(':
        should_run = True

    if should_run is False:
        # write </expressionList>
        write_tag(tag="expressionList",is_closed=True)

        return current_index, token, num_args

    process_expression()

    num_args += 1

    while token['tag'] == 'symbol' and token['value'] == ',':
        # write <symbol> , </symbol>
        write_token()

        current_index, token = get_next_token(i=current_index)

        process_expression()

        num_args += 1

    # write </expressionList>
    write_tag(tag="expressionList",is_closed=True)

    return num_args

def process_variable_declaration():
    """
    Purpose:
        process variable declaration

    Arguments:
        None

    Return:
        None
    """
    global token, current_index
    verify_token_and_current_index()
    # write <varDec>
    write_tag(tag="varDec",is_closed=False)

    verify_token_type(expected_tokens=[{'tag':'keyword','value':'var'}])

    # write <keyword> var </keyword>
    write_token()
    
    # get next token
    current_index, token = get_next_token(i=current_index)

    verify_token_type(
        expected_tokens=[
            {'tag':'keyword','value':'int'},
            {'tag':'keyword','value':'char'},
            {'tag':'keyword','value':'boolean'},
            {'tag':'identifier'}
        ]
    )

    id_type = token['value']

    # write <keyword> int or boolean or char </keyword> OR <identifier> className </identifier>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'identifier'}])

    id_name = token['value']

    var_classification = ""
    if id_type in ("char","boolean","int"):
        var_classification = "variable"
    else:
        var_classification = "object"

    add_to_symbol_table(
        name=id_name,
        id_type=id_type,
        kind="local",
        var_classification=var_classification,
        is_class_level=False
    )

    # write <identifier> varName </identifier>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    while token['tag'] == 'symbol' and token['value'] == ',':
        # write <symbol> , </symbol>
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

        verify_token_type(expected_tokens=[{'tag':'identifier'}])

        id_name = token['value']

        add_to_symbol_table(
            name=id_name,
            id_type=id_type,
            kind="local",
            var_classification=var_classification,
            is_class_level=False
        )

        # write <identifier> varName </identifier>
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'symbol','value':';'}])

    # write <symbol> ; </symbol>
    write_token()

    # write </varDec>
    write_tag(tag="varDec",is_closed=True)

    # get next token
    current_index, token = get_next_token(i=current_index)

def process_parameter_list():
    """
    Purpose:
        process subroutine declaration
    Arguments:
        None
    Return:
        None
    """
    global token, current_index
    verify_token_and_current_index()
    # write <parameterList>
    write_tag(tag="parameterList",is_closed=False)
    
    if (token['tag'] == "keyword" and \
        (token['value'] == "int" or token['value'] == "char" or\
        token['value'] == "boolean")) or (token['tag'] == 'identifier'):
        # write <keyword> data type </keyword> or <identifier> className </identifier> token
        write_token()

        id_type = token['value']

        # get next token
        current_index, token = get_next_token(i=current_index)

        verify_token_type(expected_tokens=[{'tag':'identifier'}])

        id_name = token['value']

        var_classification = ""

        if id_type in ("int","char","boolean"):
            var_classification = "variable"
        else:
            var_classification = "object"

        add_to_symbol_table(
            name=id_name,
            id_type=id_type,
            kind="argument",
            var_classification=var_classification,
            is_class_level=False
        )

        # write <identifier> argument Name </identifier>
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

        while token['tag'] == 'symbol' and token['value'] == ',':
            # write <symbol> , </symbol>
            write_token()

            # get next token
            current_index, token = get_next_token(i=current_index)

            verify_token_type(
                expected_tokens=[
                    {'tag':'keyword','value':'int'},
                    {'tag':'keyword','value':'char'},
                    {'tag':'keyword','value':'boolean'},
                    {'tag':'identifier'},
                ]
            )

            id_type = token['value']

            # write <keyword> data type </keyword> or <identifier> className </identifier> token
            write_token()

            # get next token
            current_index, token = get_next_token(i=current_index)

            verify_token_type(expected_tokens=[{'tag':'identifier'}])

            id_name = token['value']

            if id_type in ("int","char","boolean"):
                var_classification = "variable"
            else:
                var_classification = "object"

            add_to_symbol_table(
                name=id_name,
                id_type=id_type,
                kind="argument",
                var_classification=var_classification,
                is_class_level=False
            )

            # write <identifier> argument Name </identifier>
            write_token()

            # get next token
            current_index, token = get_next_token(i=current_index)

    # write </parameterList>
    write_tag(tag="parameterList",is_closed=True)

def process_class_var_declaration():
    """
    Purpose:
        process class variable declaration

    Arguments:
        None
    Return:
        None
    """
    global current_index, token
    verify_token_and_current_index()

    # write <classVarDec>
    write_tag(tag="classVarDec",is_closed=False)

    verify_token_type(
        expected_tokens=[
            {'tag':'keyword','value':'static'},
            {'tag':'keyword','value':'field'}
        ]
    )

    kind = token['value'].replace(" ","")

    # write <keyword> static OR field </keyword>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    verify_token_type(
        expected_tokens=[
            {'tag':'keyword','value':'int'},
            {'tag':'keyword','value':'char'},
            {'tag':'keyword','value':'boolean'},
            {'tag':'identifier'}
        ]
    )

    id_type = token['value'].replace(" ","")

    # write <keyword> data  type </keyword> OR <identifier> className </identifier>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'identifier'}])

    id_name = token['value'].replace(" ","")

    var_classification = ""

    if id_type in ("int","char","boolean"):
        var_classification = "variable"
    else:
        var_classification = "object"

    # write <identifier> identifier name </identifier>
    write_token()

    # get next token
    current_index, token = get_next_token(i=current_index)

    add_to_symbol_table(
        name=id_name,
        id_type=id_type,
        kind=kind,
        var_classification=var_classification,
        is_class_level=True
    )

    while token['tag'] == 'symbol' and token['value'] == ',':
        verify_token_type(expected_tokens=[{'tag':'symbol','value':','}])
        # write <symbol> , </symbol>
        write_token()

        # get next token
        current_index, token = get_next_token(i=current_index)

        verify_token_type(expected_tokens=[{'tag':'identifier'}])

        id_name = token['value'].replace(" ","")

        add_to_symbol_table(
            name=id_name,
            id_type=id_type,
            var_classification=var_classification,
            kind=kind,
            is_class_level=True
        )

        # write <identifier> identifier name </identifier>
        write_token()

        # get next token
        current_index,token=get_next_token(i=current_index)

    verify_token_type(expected_tokens=[{'tag':'symbol','value':';'}])

    # write <symbol> ; </symbol>
    write_token()

    # write </classVarDec>
    write_tag(tag="classVarDec",is_closed=True)

    # get next token
    current_index, token = get_next_token(i=current_index)

def generate_token_list():
    """
    Purpose:
        Generate token list from input file

    Arguments:
        None

    Return:
        None
    """
    global token_list, input_file
    try:
        assert isinstance(input_file,str)
        tree = ET.parse(input_file)

        root = tree.getroot()

        data = []

        for child in root:
            value = (child.text).replace(" ","")
            tag = child.tag

            data.append({
                'tag': tag,
                'value': value
            })

        token_list = data
    except AssertionError:
        print("Error: ")
        print("Invalid arguments")
        print(f"token_list = {token_list}")
        print(f"input_file = {input_file}")
        sys.exit()

def get_next_token(i):
    """
    Purpose:
        Retrieve next token from token list

    Arguments:
        i : int
            index to retrieve

    Return:
        current_index:
            updated index

        token:
            token in token list
    """
    global token_list
    try:
        assert isinstance(i,int)
        assert isinstance(token_list,list)
        for e in token_list:
            assert isinstance(e,dict)
            assert 'tag' in e and 'value' in e
        t = i + 1
        return t,token_list[t]
    except AssertionError:
        print("Error: ")
        print("invalid arguments")
        print(f"i = {i}")
        print(f"token_list = {token_list}")
        sys.exit()

def start_parse(filename):
    """
    Purpose:
        This function will start the parsing process

    Arguments:
        filename : str
            file or directory name

    Return:
        None
    """
    global input_file, output_file, token, current_index
    try:
        assert isinstance(filename,str)
        # check if directory
        if os.path.isdir(filename):
            # get directory name
            dir_name = filename

            # iterate over files
            for file in os.listdir(dir_name):
                # get file
                if file.endswith("T.xml"):
                    output_file_name = file.split('/')[-1].split('.')[0]
                    output_file_name = output_file_name[0:len(output_file_name)-1]
                    original_name = output_file_name
                    output_file_name = f"{dir_name}/{output_file_name}.pxml"
                    input_file = f"{filename}/{file}"
                    generate_token_list()
                    current_index = -1
                    current_index, token = get_next_token(i=current_index)
                    output_file = output_file_name
                    process_class()

                    output_file_name2 = os.path.join(dir_name,f"{original_name}.xml")
                    if os.path.isfile(output_file_name2):
                        os.remove(output_file_name2)
                    os.rename(output_file_name,output_file_name2)
        else:
            # get single filename
            input_file = filename
            # get filename without extension
            filename = input_file.split('/')[-1].split('.')[0]
            # output file name
            filename = filename[0:len(filename)-1]
            original_name = filename
            output_file_name = f"{filename}.pxml"
            generate_token_list()
            current_index = -1
            current_index, token = get_next_token(i=current_index)
            output_file = output_file_name

            process_class()

            output_file_name2 = f"{original_name}.xml"
            if os.path.isfile(output_file_name2):
                os.remove(output_file_name2)
            os.rename(output_file_name,output_file_name2)
    except AssertionError:
        print("Error: ")
        print("Invalid arguments")
        print(f"filename = {filename}")
        sys.exit()

def main():
    """
    Purpose:
        Main function. Entry point of program
    Arguments:
        None
    Return:
        None
    """

    try:
        n = len(sys.argv)

        assert n == 2
        # get filename
        filename = sys.argv[1]

        start_parse(filename=filename)
    except AssertionError:
        print("Error: Missing arguments")
        print("Program should be run as: <program name> <xml file or directory>")
        sys.exit()

if __name__ == "__main__":
    main()
