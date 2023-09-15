""" The lang module contains all the relevant code necessary to parse Assemblome files"""

## Imports

import re

## Constants

# REGEXES to detect the main instructions of Assemblome 
# Import : 'import flsy as polypeptide'
# Tag: 'tag "FLSY.aa" as polypeptide'
# Functional expression: 'oKI@FLSY.aa'

REGEX_IMPORT =  r'^import (?P<path_import>[^"]+) as (?P<tag>\w+)$'
REGEX_TAG = r'^tag "(?P<data>[^"]+)" as (?P<tag>\w+)$'
REGEX_FUNCTIONAL_EXPRESSION = r'([A-Za-z0-9+/=]+)@([ARNDCQEGHILKMFPSTWYV]+)\.aa'

## Functions

def find_import_pattern(text):
    path_import, tag = None, None

    match = re.fullmatch(REGEX_IMPORT, text)

    if match:
        path_import = match.group('path_import')
        tag = match.group('tag')

    return path_import, tag

def find_tag_pattern(text):
    """detect tag patterns"""
    data, tag = None, None

    # Match the pattern in the text
    match = re.fullmatch(REGEX_TAG, text)

    if match:
        data = match.group('data')
        tag = match.group('tag')

    return data, tag

def load_import(path_import):
    with open(path_import, 'r') as file:
        content = ''.join(list(map(str.strip, file)))

    return content

# TODO: Creeate a single backawards file replacement mechanism for both imports and tags
# They are basically the same

def parse_imports(content):
    """replace all tags by their corresponding data following the tag instructions"""
    content_new = []

    for i, line in sorted(enumerate(content), key=lambda x: x[0], reverse=True):
        path_import, tag = find_import_pattern(line)
        if path_import is not None and tag is not None:
            content_import = load_import(path_import)
            content_new = [line.replace(tag, content_import) for line in content_new]
        else:
            content_new.append(line)

    content_new.reverse()
    return content_new

def parse_tags(content):
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
