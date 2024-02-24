"""
This module will parse an XML file that contains tokens
and will add the context of class, procedures, variables, and so on
This is based on the nand2tetris book
"""
import sys
import os
import xml.etree.ElementTree as ET


def write_tag(output_file: str, tag: str, is_closed: bool) -> None:
    """
    Purpose:
        write opening or closing tag

    Argument:
        output_file:
            output file path

        tag:
            tag to write

        is_closed:
            boolean flag to determine if write closed tag or open tag
    """

    with open(output_file,"a+",encoding="utf-8") as f:
        if is_closed is True:
            f.write(f"</{tag}>\n")
        else:
            f.write(f"<{tag}>\n")


def write_token(output_file:str, token:dict[str,str]) -> None:
    """
    Purpose:
        write value enclosed between tags

    Arguments:
        output_file:
            output file path

        token:
            dictionary of type:
            {
                tag: str,
                value: str
            }
            where tag is XML tag and value is tag value

    Return:
        None
    """
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


def verify_token_type(
        actual_token : dict[str,str],
        expected_tokens : list[dict[str,str]],
        input_file : str
    )->None:
    """
    Purpose:
        verify that token matches expected value

    Argument:
        actual_token:
            token to check
            dictionary of type{
                tag: string,
                value: string
            }

        expected_token:
            list token to compare to where each entry is of form
            dictionary of type{
                tag: string,
                value: string
            }

        input_file:
            input file path

    Return:
        None
    """
    try:
        valid = False
        for e in expected_tokens:
            if 'value' in e.keys():
                valid = (actual_token['tag'] == e['tag'] and actual_token['value'] == e['value'])
            else:
                valid = actual_token['tag'] == e['tag']

            if valid:
                break

        assert valid is True
    except AssertionError:
        print("Error: Invalid token")
        print(f"File: {input_file}")
        print(f"Received tag: {actual_token['tag']}")
        print(f"Received value: {actual_token['value']}")

        c = 0
        for e in expected_tokens:
            print(f"Expected tag: {e['tag']}")
            if 'value' in e.keys():
                print(f"with Expected value: {e['value']}")
            if c + 1 < len(expected_tokens):
                print("OR")
            c += 1
        sys.exit()

def process_class(
        output_file: str,
        token: dict[str,str],
        token_list: list[dict[str,str]],
        current_index : int,
        input_file : str
    )->tuple[int,dict[str,str]]:
    """
    Purpose:
        process class

    Arguments:
        output_file:
            output file path

        token:
            dictionary of form:
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens

        current_index:
            current_index processed by token list

        input_file:
            input file path
    Return:
        current_index, token
    """
    # write <class> tag
    write_tag(output_file=output_file,tag="class",is_closed=False)

    # verify if tag is class else raise Exception
    verify_token_type(actual_token=token,expected_tokens=[{'tag':'keyword','value':'class'}],input_file=input_file)

    # write <keyword> class </keyword> token
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    # verify if tag is class else raise Exception
    verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

    # write <identifer> className </identifier> token
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    # verify if tag is class else raise Exception
    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'{'}],input_file=input_file)

    # write <symbol> { </symbol> token
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    while token['tag'] == "keyword" and (token['value'] == "static" or token["value"] == "field"):
        # process variable declaration
        current_index,token = process_class_var_declaration(
            output_file=output_file,
            token=token,
            token_list=token_list,
            current_index=current_index,
            input_file=input_file
        )

    while token['tag'] == "keyword" and \
    (token['value'] == "constructor" or token['value'] == "function" or \
     token['value'] == "method"):
        # process subroutine declaration
        current_index,token = process_subroutine_declaration(
            output_file=output_file,
            token=token,
            token_list=token_list,
            current_index=current_index,
            input_file=input_file
        )


    # verify if tag is class else raise Exception
    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'}'}],input_file=input_file)

    # write <symbol> } </symbol> token
    write_token(output_file=output_file,token=token)

    # write </class>
    write_tag(output_file=output_file,tag="class",is_closed=True)

    return current_index, token

def process_subroutine_declaration(
    output_file : str,
    token : dict[str,str],
    token_list : list[dict[str,str]],
    current_index : int,
    input_file : str
) -> tuple[int, dict[str,str]]:
    """
    Purpose:
        process subroutine declaration

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

        input_file:
            input file path

    Return:
        current_index and next token
    """
    # write <subroutineDec>
    write_tag(output_file=output_file,tag="subroutineDec",is_closed=False)

    verify_token_type(actual_token=token,expected_tokens=[
        {'tag': 'keyword', 'value': 'constructor'},
        {'tag': 'keyword', 'value': 'function'},
        {'tag': 'keyword', 'value': 'method'}
    ],input_file=input_file)

    # write <keyword> constructor OR function OR method </keyword>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[
        {'tag':'keyword','value':'void'},
        {'tag':'keyword','value':'int'},
        {'tag':'keyword','value':'char'},
        {'tag':'keyword','value':'boolean'},
        {'tag':'identifier'},
    ],input_file=input_file)

    # write <keyword> void OR int OR char OR boolean </keyword>
    # OR <identifier> className </identifier>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

    # write <identifier> subprocedure name </identifier>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'('}],input_file=input_file)

    # write <symbol> ( </symbol>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    current_index, token = process_parameter_list(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':')'}],input_file=input_file)

    # write <symbol> ) </symbol>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    current_index, token = process_subroutine_body(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    # write </subroutineDec>
    write_tag(output_file=output_file,tag="subroutineDec",is_closed=True)

    return current_index, token

def process_subroutine_body(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process subroutine body

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

        input_file:
            input file path
    Return:
        current_index and next token
    """

    # write <subroutineBody>
    write_tag(output_file=output_file,tag="subroutineBody",is_closed=False)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'{'}],input_file=input_file)

    # write <symbol> { </symbol>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    while token['tag'] == 'keyword' and token['value'] == 'var':
        current_index, token = process_variable_declaration(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    current_index, token = process_statements(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'}'}],input_file=input_file)

    # write <symbol> } </symbol>
    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    # write </subroutineBody>
    write_tag(output_file=output_file,tag="subroutineBody",is_closed=True)

    return current_index, token

def process_statements(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process statements

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

        input_file:
            input file path
    Return:
        current_index and next token
    """
    # write <statements>
    write_tag(output_file=output_file,tag="statements",is_closed=False)

    while token['tag'] == 'keyword' and (token['value'] == 'let' or token['value'] == 'if' or token['value'] == 'while' or token['value'] == 'do' or token['value'] == 'return'):
        if token['tag'] == 'keyword' and token['value'] == 'let':
            current_index, token = process_let_statement(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
        elif token['tag'] == 'keyword' and token['value'] == 'if':
            current_index, token = process_if_statement(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
        elif token['tag'] == 'keyword' and token['value'] == 'while':
            current_index, token = process_while_statement(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
        elif token['tag'] == 'keyword' and token['value'] == 'do':
            current_index, token = process_do_statement(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
        elif token['tag'] == 'keyword' and token['value'] == 'return':
            current_index, token = process_return_statement(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    # write </statements>
    write_tag(output_file=output_file,tag="statements",is_closed=True)

    return current_index, token

def process_while_statement(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process while statements

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

        input_file:
            input file path

    Return:
        current_index and next token
    """
    # write <whileStatement>
    write_tag(output_file=output_file,tag="whileStatement",is_closed=False)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'keyword','value':'while'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'('}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    current_index, token = process_expression(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':')'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'{'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    current_index, token = process_statements(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'}'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    # write </whileStatement>
    write_tag(output_file=output_file,tag="whileStatement",is_closed=True)

    return current_index, token


def process_if_statement(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process if statements

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

        input_file:
            input file path    
    Return:
        current_index and next token
    """
    # write <ifStatement>
    write_tag(output_file=output_file,tag="ifStatement",is_closed=False)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'keyword','value':'if'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'('}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    current_index, token = process_expression(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
    
    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':')'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'{'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    current_index, token = process_statements(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
    
    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'}'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    if token['tag'] == 'keyword' and token['value'] == 'else':
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)
        
        verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'{'}],input_file=input_file)

        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)

        current_index, token = process_statements(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'}'}],input_file=input_file)

        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)

    # write </ifStatement>
    write_tag(output_file=output_file,tag="ifStatement",is_closed=True)

    return current_index, token


def process_do_statement(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process return statements

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

        input_file:
            input file path

    Return:
        current_index and next token
    """
    # write <doStatement>
    write_tag(output_file=output_file,tag="doStatement",is_closed=False)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'keyword','value':'do'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    current_index, token = process_subroutine_call(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':';'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    # write </doStatement>
    write_tag(output_file=output_file,tag="doStatement",is_closed=True)

    return current_index, token


def process_return_statement(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process return statements

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

        input_file:
            input file path

    Return:
        current_index and next token
    """
    # write <returnStatement>
    write_tag(output_file=output_file,tag="returnStatement",is_closed=False)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'keyword','value':'return'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    if token['tag'] == 'integerConstant' or \
    token['tag'] == 'stringConstant' or \
    token['tag'] == 'keyword' and \
    (token['value'] == 'true' or token['value'] == 'false' or \
    token['value'] == 'null' or token['value'] == 'this') or \
    token['tag'] == 'identifier' or \
    token['tag'] == 'symbol' and (token['value'] == '-' or token['value'] == '~') or \
    token['tag'] == 'symbol' and token['value'] == '(':
        current_index, token = process_expression(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':';'}],input_file=input_file)

    write_token(output_file=output_file,token=token)

    current_index, token = get_next_token(token_list=token_list,i=current_index)

    # write </returnStatement>
    write_tag(output_file=output_file,tag="returnStatement",is_closed=True)

    return current_index, token


def process_let_statement(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process statements

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

        input_file:
            input file path

    Return:
        current_index and next token
    """
    # write <letStatement>
    write_tag(output_file=output_file,tag="letStatement",is_closed=False)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'keyword','value':'let'}],input_file=input_file)

    # write <keyword> let </keyword> token
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

    # write <identifier> varName </identifier>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    if token['tag'] == 'symbol' and token['value'] == '[':
        # write <symbol> [ </symbol>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)

        current_index, token = process_expression(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':']'}],input_file=input_file)

        # write <symbol> ] </symbol>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)


    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'='}],input_file=input_file)

    # write <symbol> = </symbol>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    current_index, token = process_expression(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':';'}],input_file=input_file)

    # write <symbol> ; </symbol>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    # write </letStatement>
    write_tag(output_file=output_file,tag="letStatement",is_closed=True)

    return current_index, token

def process_expression(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process expression

    Arguments:
        output_file:
            output file path

        token:
            dictionary of form 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens

        current_index:
            current index

        input_file:
            input file path

    Return:
        current index and tokens
    """
    # write <expression>
    write_tag(output_file=output_file,tag="expression",is_closed=False)

    #print(f"process expression received = {token}")

    current_index, token = process_term(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    while token['tag'] == 'symbol' and \
        (token['value'] == '+' or token['value'] == '-' or \
         token['value'] == '*' or token['value'] == '/' or \
        token['value'] == '&' or token['value'] == '|' or \
        token['value'] == '<' or token['value'] == '>' or \
        token['value'] == '='):

        # write operator
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)

        # process term
        current_index, token = process_term(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
    
    # write </expression>
    write_tag(output_file=output_file,tag="expression",is_closed=True)

    return current_index, token

def process_term(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process expression

    Arguments:
        output_file:
            output file path

        token:
            dictionary of form 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens

        current_index:
            current index

        input_file:
            input file path
    Return:
        current index and tokens
    """
    # write <term>
    #print(f"process term received token={token}")

    write_tag(output_file=output_file,tag="term",is_closed=False)

    if token['tag'] == 'integerConstant':
        # write <integerConstant> int constant </integerConstant>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)
    elif token['tag'] == 'stringConstant':
        # write <stringConstant> string constant </stringConstant>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)
    elif token['tag'] == 'keyword' and (token['value'] == 'true' or token['value'] == 'false' or token['value'] == 'null' or token['value'] == 'this'):
        # write <keyword> true OR false OR null OR this </keyword>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)
    elif token['tag'] == 'identifier':
        next_index, next_token = get_next_token(token_list=token_list,i=current_index)

        if next_token['tag'] == 'symbol' and next_token['value'] == '[':
            # write <identifier> var name </identifier>
            write_token(output_file=output_file,token=token)

            token=next_token
            current_index=next_index

            verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'['}],input_file=input_file)

            # write <symbol> [ </symbol>
            write_token(output_file=output_file,token=token)

            current_index, token = get_next_token(token_list=token_list,i=current_index)

            current_index, token = process_expression(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

            verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':']'}],input_file=input_file)

            # write <symbol> ] </symbol>
            write_token(output_file=output_file,token=token)

            current_index, token = get_next_token(token_list=token_list,i=current_index)
        elif next_token['tag'] == 'symbol' and (next_token['value'] == '(' or next_token['value'] == '.'):
            current_index, token = process_subroutine_call(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
        else:
            # write <identifier> var name </identifier>
            write_token(output_file=output_file,token=token)

            token=next_token
            current_index=next_index
    # check if dealing with unaryOp (- or ~)
    elif token['tag'] == 'symbol' and (token['value'] == '-' or token['value'] == '~'):
        # write <symbol> ~ OR - </symbol>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)

        current_index, token = process_term(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
    
    elif token['tag'] == 'symbol' and token['value'] == '(':
        # write <symbol> ( </symbol>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)

        current_index, token = process_expression(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':')'}],input_file=input_file)

        # write <symbol> ) </symbol>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)


    # write </term>
    write_tag(output_file=output_file,tag="term",is_closed=True)

    return current_index, token

def process_subroutine_call(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process subroutine call

    Arguments:
        output_file:
            output file path

        token:
            dictionary of form 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens

        current_index:
            current index

        input_file:
            input file path

    Return:
        current index and tokens
    """
    verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)
    # write <identifier> subroutine name or class name or var name </identifier>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    if token['tag'] == 'symbol' and token['value'] == '(':
        # write <symbol> ( </symbol>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)

        #print(f"token = {token}")

        current_index, token = process_expression_list(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':')'}],input_file=input_file)

        # write <symbol> ) </symbol>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)
    elif token['tag'] == 'symbol' and token['value'] == '.':
        # write <symbol> . </symbol>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

        # write <identifier> subroutine name </identifier>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':'('}],input_file=input_file)

        # write <symbol> ( </symbol>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)

        current_index, token = process_expression_list(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':')'}],input_file=input_file)

        # write <symbol> ) </symbol>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)
    
    return current_index, token

def process_expression_list(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process subroutine call

    Arguments:
        output_file:
            output file path

        token:
            dictionary of form 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens

        current_index:
            current index

        input_file:
            input file path

    Return:
        current index and tokens
    """
    # write <expressionList>
    write_tag(output_file=output_file,tag="expressionList",is_closed=False)

    should_run = False

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
        write_tag(output_file=output_file,tag="expressionList",is_closed=True)

        return current_index, token

    current_index, token = process_expression(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    while token['tag'] == 'symbol' and token['value'] == ',':
        # write <symbol> , </symbol>
        write_token(output_file=output_file,token=token)

        current_index, token = get_next_token(token_list=token_list,i=current_index)

        current_index, token = process_expression(output_file=output_file,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

    # write </expressionList>
    write_tag(output_file=output_file,tag="expressionList",is_closed=True)

    return current_index, token

def process_variable_declaration(
        output_file : str,
        token : dict[str,str],
        token_list : list[dict[str,str]],
        current_index : int,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process variable declaration

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

    Return:
        current_index and next token
    """
    # write <varDec>
    write_tag(output_file=output_file,tag="varDec",is_closed=False)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'keyword','value':'var'}],input_file=input_file)

    # write <keyword> var </keyword>
    write_token(output_file=output_file,token=token)
    
    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[
        {'tag':'keyword','value':'int'},
        {'tag':'keyword','value':'char'},
        {'tag':'keyword','value':'boolean'},
        {'tag':'identifier'},
    ],input_file=input_file)

    # write <keyword> int or boolean or char </keyword> OR <identifier> className </identifier>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

    # write <identifier> varName </identifier>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    while token['tag'] == 'symbol' and token['value'] == ',':
        # write <symbol> , </symbol>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

        # write <identifier> varName </identifier>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':';'}],input_file=input_file)

    # write <symbol> ; </symbol>
    write_token(output_file=output_file,token=token)

    # write </varDec>
    write_tag(output_file=output_file,tag="varDec",is_closed=True)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    return current_index, token

def process_parameter_list(
        output_file : str,
        token: dict[str,str],
        token_list: list[dict[str,str]],
        current_index : str,
        input_file : str
    ) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process subroutine declaration

    Arguments:
        output_file:
            output file path

        token:
            token of type 
            {
                tag: str,
                value: str
            }

        token_list:
            list of tokens to process

        current_index:
            current index processed

        input_file:
            input file path

    Return:
        current_index and next token
    """

    # write <parameterList>
    write_tag(output_file=output_file,tag="parameterList",is_closed=False)
    
    if (token['tag'] == "keyword" and (token['value'] == "int" or token['value'] == "char" or token['value'] == "boolean")) or (token['tag'] == 'identifier'):
        # write <keyword> data type </keyword> or <identifier> className </identifier> token
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

        # write <identifier> argument Name </identifier>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)

        while token['tag'] == 'symbol' and token['value'] == ',':
            # write <symbol> , </symbol>
            write_token(output_file=output_file,token=token)

            # get next token
            current_index, token = get_next_token(token_list=token_list,i=current_index)

            verify_token_type(actual_token=token,expected_tokens=[
                {'tag':'keyword','value':'int'},
                {'tag':'keyword','value':'char'},
                {'tag':'keyword','value':'boolean'},
                {'tag':'identifier'},
            ],input_file=input_file)

            # write <keyword> data type </keyword> or <identifier> className </identifier> token
            write_token(output_file=output_file,token=token)

            # get next token
            current_index, token = get_next_token(token_list=token_list,i=current_index)

            verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

            # write <identifier> argument Name </identifier>
            write_token(output_file=output_file,token=token)

            # get next token
            current_index, token = get_next_token(token_list=token_list,i=current_index)

    # write </parameterList>
    write_tag(output_file=output_file,tag="parameterList",is_closed=True)

    return current_index, token

def process_class_var_declaration(
    output_file: str,
    token: dict[str,str],
    token_list: list[dict[str,str]],
    current_index: int,
    input_file : str
) -> tuple[int,dict[str,str]]:
    """
    Purpose:
        process class variable declaration

    Arguments:
        output_file:
            output file path

        token_list:
            list of tokens

        token:
            current token processed of form
            {
                tag: str,
                value: str
            }

        current_index:
            current_index processed by token list

        input_file:
            input file path
    Return:
        current_index:
            updated index

        token:
            next token to process
    """
    # write <classVarDec>
    write_tag(output_file=output_file,tag="classVarDec",is_closed=False)

    verify_token_type(actual_token=token,expected_tokens=[
        {'tag':'keyword','value':'static'},
        {'tag':'keyword','value':'field'}
    ],input_file=input_file)

    # write <keyword> static OR field </keyword>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[
        {'tag':'keyword','value':'int'},
        {'tag':'keyword','value':'char'},
        {'tag':'keyword','value':'boolean'},
        {'tag':'identifier'}
    ],input_file=input_file)

    # write <keyword> data  type </keyword> OR <identifier> className </identifier>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

    # write <identifier> identifier name </identifier>
    write_token(output_file=output_file,token=token)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    while token['tag'] == 'symbol' and token['value'] == ',':
        verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':','}],input_file=input_file)
        # write <symbol> , </symbol>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index, token = get_next_token(token_list=token_list,i=current_index)

        verify_token_type(actual_token=token,expected_tokens=[{'tag':'identifier'}],input_file=input_file)

        # write <identifier> identifier name </identifier>
        write_token(output_file=output_file,token=token)

        # get next token
        current_index,token=get_next_token(token_list=token_list,i=current_index)

    verify_token_type(actual_token=token,expected_tokens=[{'tag':'symbol','value':';'}],input_file=input_file)

    # write <symbol> ; </symbol>
    write_token(output_file=output_file,token=token)

    # write </classVarDec>
    write_tag(output_file=output_file,tag="classVarDec",is_closed=True)

    # get next token
    current_index, token = get_next_token(token_list=token_list,i=current_index)

    return current_index, token

def generate_token_list(input_file:str)->list[dict[str,str]]:
    """
    Purpose:
        Generate token list from input file

    Arguments:
        input_file:
            input file path

    Return:
        None
    """
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

    return data

def get_next_token(token_list:list[dict],i:int)->tuple[int,dict[str,str]]:
    """
        Purpose:
            Retrieve next token from token list

        Arguments:
            token_list:
                list of tokens

            i:
                index to retrieve

        Return:
            current_index:
                updated index

            token:
                token in token list
    """
    t = i + 1
    return t,token_list[t]

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
    except AssertionError:
        print("Error: Missing arguments")
        print("Program should be run as: <program name> <xml file or directory>")
        sys.exit()
    # get filename
    filename = sys.argv[1]

    # check if directory
    if os.path.isdir(filename):
        # get directory name
        dir_name = sys.argv[1]

        # iterate over files
        for file in os.listdir(dir_name):
            # get file
            if file.endswith("T.xml"):
                output_file_name = file.split('/')[-1].split('.')[0]
                output_file_name = f"{output_file_name}TEST.xml"
                input_file = f"{filename}/{file}"
                token_list = generate_token_list(input_file=input_file)
                current_index = -1
                current_index, token = get_next_token(token_list=token_list,i=current_index)
                current_index, token = process_class(output_file=output_file_name,token=token,token_list=token_list,current_index=current_index,input_file=input_file)
    else:
        # get single filename
        input_file = sys.argv[1]
        # get filename without extension
        filename = input_file.split('/')[-1].split('.')[0]
        print(f"input_file={input_file}")
        # output file name
        output_file_name = f"{filename}TTest.xml"
        token_list = generate_token_list(input_file=input_file)
        current_index = -1
        current_index, token = get_next_token(token_list=token_list,i=current_index)

        current_index, token = process_class(output_file=output_file_name,token=token,token_list=token_list,current_index=current_index,input_file=input_file)

if __name__ == "__main__":
    main()
