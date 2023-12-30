"""This module contains the parser that will compile the assemblome code towards the desired architecture: DNA or RNA"""

### Imports
import re
from utils import *

### Patterns

REGEX_SLIPPERY = r'([AUGC]+)\.rna\s+(<+|>+)\s+([AUGC]+)\.rna'
REGEX_PRODUCE = r'produce ([AUGC]+)\.rna'
#REGEX_RNA = r'([AUGC]+)\.rna'

### Functions

def replace_slippery_sequence(match):
    """Process slippery sequences.
    rna1 < rna2 means rna2 is the version obtained when there is a -1 slip when translating rna1
    rna1 << rna2 is the same for a -2 slip
    TO-DO: handle positive slips with > """

    rna1 = match.group(1)
    stream = match.group(2)
    rna2 = match.group(3)

    stream_type = '<' if '<' in stream else '>'
    stream_count = len(stream)
    
    # If there is a negative slip, it means rna2 has too much of some nucleotides, as a subseq got repeated
    if stream_type == '<':
        # First, retrieve everything before the -1 PFR
        part_first = common_start(rna1, rna2)
        part_second = None
        # Second, retrieve the end of each rna seq and ignore the duplicated part of rna2
        # Assuming there is no other slippery event
        # One of the end should be entirely included in the other
        end_rna1, end_rna2 = rna1[len(part_first):], rna2[len(part_first)+stream_count:]
        if len(end_rna2) >= len(end_rna1):
            if end_rna1 not in end_rna2:
                raise Exception("Error: not a slippery event")
            else:
                part_second = end_rna2
        else:
            if end_rna2 not in end_rna1:
                raise Exception("Error: not a slippery event")
            else:
                part_second = end_rna1
    
    return part_first + part_second + ".rna"

def replace_produce(match_obj):
    rna_chain = match_obj.group(1)
    dna_chain = rna_chain.replace('U', 'T')
    return dna_chain

### Parser

class ParserCompiler():

    def __init__(self):
        self.content = None

    def parse(self, content):
        self.content = content
        self.content = re.sub(REGEX_SLIPPERY, replace_slippery_sequence, self.content)
        self.content = re.sub(REGEX_PRODUCE, replace_produce, self.content)
        return self.content

### Tests

def test_slippery_pattern():
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

