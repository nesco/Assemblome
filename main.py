import re

from lang import parse_tags, parse_imports, parse_functional_expressions


def scan(path):
    """read a asb file and perform a lexical analysis."""
    
    instructions = ['#', 'import', 'tag', 'produce', 'raw']
    content = []
    # Placeholder lists to store tags and relationships
    tags = {}
    relationships = {}
    
    #Read file
    with open(path, 'r') as file:
        content = list(map(str.strip, file))

    content = [line for line in content if not line.startswith("#") and not line == ""]
    return content

def parse(content):
    return parse_functional_expressions(parse_tags(parse_imports(content)))

if __name__ == '__main__':
    content = scan('instruct.asb')
    output = parse(content)
