import re

# from langs import parse_tags, parse_imports, parse_functional_expressions, parse_produce
from langs import *


def scan(path):
    """read a asb file and perform a lexical analysis."""
    
    instructions = ['#', 'import', 'tag', 'produce', 'raw']
    content = []
    
    #Read file
    with open(path, 'r') as file:
        content = list(map(str.strip, file))

    content = [line for line in content if not line.startswith("#") and not line == ""]
    return content

def parse(content):
    return parse_produce(parse_functional_expressions(parse_tags(parse_imports(content))))

if __name__ == '__main__':
    content = scan('instruct.asb')
    output = parse(content)
    output_old = parse_functional_expressions(parse_tags(parse_imports(content)))
