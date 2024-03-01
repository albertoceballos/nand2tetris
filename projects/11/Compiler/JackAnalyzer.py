"""
Entry point of program
Called by autograder
"""
import sys
from jack_tokenizer import start_tokenize
from jack_parser import start_parse

def main():
    """
    Purpose:
        Entry point of program

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

    start_tokenize(filename=filename)
    start_parse(filename=filename)

if __name__ == "__main__":
    main()
