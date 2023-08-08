
def scan(path):
    """read a asb file and perform a lexical analysis."""
    
    instructions = ['produce', 'raw']
    
    with open(path, 'r') as file:
        content = list(file)
    
    return content

