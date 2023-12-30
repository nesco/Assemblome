""" This module is made to encapsulate all the preprocessing part of Assemblome:
- reads: "!read <filename> as <placeholder>"
- tags: "!tag <data> as <placeholder>"
etc
"""

import re

from utils import load_raw

#### Regular Expressions
REGEX_READ =  r'^\s*!read (?P<data>[^"]+) as (?P<tag>\w+)\s*$'
REGEX_TAG = r'^\s*!tag "(?P<data>[^"]+)" as (?P<tag>[\w-]+)\s*$'

### Utils ###

def find_replacement_pattern(text: str, regex):
    """Detect patterns which are used to replace a given token by some other data."""
    data, tag = None, None

    # Match the pattern in the text
    match = re.fullmatch(regex, text)

    if match:
        data = match.group('data')
        tag = match.group('tag')

    return data, tag

def inverse_progressive_replacement(content: list[str], regex, func: callable) -> list[str]:
    """This function replaces a sequence by another beginning by the end of the text as represented by a list of lines.
    It is used to implement aliases, as an alias should not replace sequences that are defined before it"""
    content_new = []

    for i, line in sorted(enumerate(content), key=lambda x: x[0], reverse=True):
        data, tag = find_replacement_pattern(line, regex)
        if data is not None and tag is not None:
            replacement = func(data)
            content_new = [re.sub(r"\b%s\b" % tag, replacement, line) for line in content_new] 
        else:
            content_new.append(line)

    content_new.reverse()
    return content_new

### Parser Class ###

class ParserPreprocesser():

    def __init__(self, path):
        self.path = path
        self.content = None

    def parse(self, content: list[str]) -> list[str]:
        """ Read files indicated by the !read instruction, and replace placeholders by their contents, then do the same for tags"""
        self.content = content
        self.content = inverse_progressive_replacement(self.content, REGEX_READ, lambda p: load_raw(path + p))
        self.content = inverse_progressive_replacement(self.content, REGEX_TAG, lambda x: x)
        return self.content

### Tests ###

def test_tag_replacement():
    # Happy path for tag
    content = """
    !tag "Alpha" as Alph
    !tag "Omega" as Omg
    Alph
    Omg
    I am the Alph and the Omg"""

    expected = """
    Alpha
    Omega
    I am the Alpha and the Omega"""

    parser = ParserPreprocesser(None)
    content = '\n'.join(parser.parse(content.split('\n')))
    assert content == expected

if __name__ == "__main__":
    test_tag_replacement()
