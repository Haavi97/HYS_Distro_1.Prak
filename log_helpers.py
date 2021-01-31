import sys
import logging

FORMAT = '%(asctime)-15s %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='app.log',
                    filemode='a',
                    format=FORMAT)

output = sys.stdout

def print_wl(s: str) -> str:
    """
    A wrapper function that prints to the predefined output file
    and at the same time logs an info message 

    Parameters: 
    s: str
    """

    print(s, file=output)
    logging.info(s)


def print_wl_error(s: str) -> str:
    """
    A wrapper function that prints to the std.err
    and at the same time logs an error message 

    Parameters: 
    s: str
    """

    print(s, file=sys.stderr)
    logging.error(s)