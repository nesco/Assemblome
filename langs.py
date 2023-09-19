""" The lang module contains all the relevant code necessary to parse Assemblome files"""

## Imports

import re

from utils import list_to_base64, base64_to_list
from utils_genomics import specify

## Constants

# REGEXES to detect the main instructions of Assemblome 
# Import : 'import flsy as polypeptide'
# Tag: 'tag "FLSY.aa" as polypeptide'
# Functional expression: 'oKI@FLSY.aa'

REGEX_IMPORT =  r'^import (?P<data>[^"]+) as (?P<tag>\w+)$'
REGEX_TAG = r'^tag "(?P<data>[^"]+)" as (?P<tag>\w+)$'
REGEX_FUNCTIONAL_EXPRESSION = r'([A-Za-z0-9+/=]+)@([ARNDCQEGHILKMFPSTWYV]+)\.aa'

## Functions

def find_replacement_pattern(text, regex):
    """Detect patterns which are used to replace a given token by some other data."""
    data, tag = None, None

    # Match the pattern in the text
    match = re.fullmatch(regex, text)

    if match:
        data = match.group('data')
        tag = match.group('tag')

    return data, tag

def load_import(path_import):
    with open(path_import, 'r') as file:
        content = ''.join(list(map(str.strip, file)))

    return content

def inverse_progressive_replacement(content, regex, func):
    content_new = []

    for i, line in sorted(enumerate(content), key=lambda x: x[0], reverse=True):
        data, tag = find_replacement_pattern(line, regex)
        if data is not None and tag is not None:
            replacement = func(data)
            content_new = [line.replace(tag, replacement) for line in content_new]
        else:
            content_new.append(line)

    content_new.reverse()
    return content_new
            

def parse_imports(content):
    """replace all tags by their corresponding data following the tag instructions"""
    return inverse_progressive_replacement(content, REGEX_IMPORT, load_import)

def parse_tags(content):
    """replace all tags by their corresponding data following the tag instructions"""
    return inverse_progressive_replacement(content, REGEX_TAG, lambda x: x)

def replace_functional_expression(match_obj):
    complement = match_obj.group(1)
    aa_chain = match_obj.group(2)
    rna_chain = specify(aa_chain, base64_to_list(complement)) + '.rna'
    return rna_chain

def process_functional_expression(s):
    return re.sub(REGEX_FUNCTIONAL_EXPRESSION, replace_functional_expression, s)

def parse_functional_expressions(content):
    content_new = [process_functional_expression(line) for line in content]
    return content_new
