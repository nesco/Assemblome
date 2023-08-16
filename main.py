
def scan(path):
    """read a asb file and perform a lexical analysis."""
    
    instructions = ['tag', 'produce', 'raw']
    content = []
    
    with open(path, 'r') as file:
        content = list(map(str.strip, file))
    
    return content


def parse_tag(content):
    pass

