""" The lang module contains all the relevant code necessary to parse Assemblome files"""

# TO-DO
# * TEST
# * MIGRATE ALL "PROCESS_" in a single function of higher order which applies "replace_" to content

## Imports

import re

from utils import *
from langs.preprocesser import ParserPreprocesser
from langs.converter import ParserConverter
from langs.compiler import ParserCompiler

## Functions

# Disassembly
def rna_to_functional_expression(rna_chain: str) -> str:
    aa_chain, complement = translate(rna_chain)
    return list_to_base64(complement) + "@" + aa_chain + ".aa"

def replace_rna_by_functional_expression(s):
    return re.sub(REGEX_RNA, lambda match: rna_to_functional_expression(match.group(1)), s)

#### Tests

def test_slippery():
    text = "AUGCAUGCA.rna >>> GCUAGCUA.rna"

    match = re.search(REGEX_SLIPPERY, text)
    if match:
        first_rna = match.group(1)
        stream = match.group(2)
        second_rna = match.group(3)

        stream_type = '<' if '<' in stream else '>'
        stream_count = len(stream)

        print("First RNA:", first_rna)
        print("Stream:", stream_type, "repeated", stream_count, "times")
        print("Second RNA:", second_rna)

