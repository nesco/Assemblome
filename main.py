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
    path_dir = '/'.join(path.split('/')[:-1])
    if len(path_dir) > 0:
        path_dir = path_dir + '/'
    else:
        path_dir = './'
    return content, path_dir

def parse(content, path):
    return parse_produce(parse_functional_expressions(parse_pdbs(parse_tags(parse_imports(content, path)))))

def assemble(content, path):
    content_parsed = parse(content, path)
    content_linearized = ''.join(content_parsed)

    content_tabulated = ''
    for i, caracter in enumerate(content_linearized):
        if i % 70 == 0 and i > 0:
            content_tabulated += '\n'

        content_tabulated += caracter
    
    return content_tabulated

if __name__ == '__main__':
    content, path = scan('instruct_without_pdb.asb')
    print(path)
    output = parse(content, path)
    output_old = parse_functional_expressions(parse_tags(parse_imports(content, path)))
