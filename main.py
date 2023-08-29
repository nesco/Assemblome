import re

def scan(path):
    """read a asb file and perform a lexical analysis."""
    
    instructions = ['tag', 'produce', 'raw']
    content = []
    
    with open(path, 'r') as file:
        content = list(map(str.strip, file))
    
    return content



def find_tag_pattern(text):
    """detect tag patterns"""
    data, tag = None, None

    # Define the regular expression pattern
    pattern = r'^tag "(?P<data>[^"]+)" as (?P<tag>\w+)$'

    # Match the pattern in the text
    match = re.fullmatch(pattern, text)

    if match:
        data = match.group('data')
        tag = match.group('tag')
        
    return data, tag

def parse_tag(content):
    """replace all tags by their corresponding data following the tag instructions"""
    content_new = []

    for i, line in sorted(enumerate(content), key=lambda x: x[0], reverse=True):
        data, tag = find_tag_pattern(line)
        if data is not None and tag is not None:
            content_new = [line.replace(tag, data) for line in content_new]
        else:
            content_new.append(line)

    content_new.reverse()
    return content_new
