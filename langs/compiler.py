"""This module contains the parser that will compile the assemblome code towards the desired architecture: DNA or RNA"""

### Imports
import re
from utils import *

### Patterns

REGEX_SLIPPERY = r'([AUGC]+)\.rna\s+(<+|>+)\s+([AUGC]+)\.rna'
REGEX_PRODUCE = r'produce ([AUGC]+)\.rna'
REGEX_MULTISEQUENCE = r"([AUGC]+(?:\s*\|\s*[AUGC]+)*)"
#REGEX_MULTISEQUENCE_ON_SEVERAL_LINES =   r"\(\s*([AUGC\s]+(?:\s*\|\s*[AUGC\s]+)*)\s*\)"
#r"(\(\s*([AUGC]+\.rna(?:\s*\|\s*[AUGC]+\.rna)*)\s*\))"
REGEX_RNA = r'\b([AUGC]+)\.rna\b'

### Exceptions

class InvalidMultisequenceException(Exception):
    """Exception raised when sequences cannot form a single RNA sequence."""
    def __init__(self, sequence, message="does not fit the criteria for forming a single RNA sequence."):
            self.sequence = sequence
            self.message = f"Sequence '{sequence}' {message}"
            super().__init__(self.message)

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

def capture_multisequences(content):
    content_new = content

#    patterns_multiline = re.findall(REGEX_MULTISEQUENCE_ON_SEVERAL_LINES, content_new, re.DOTALL)

#    for full_expr, pattern in patterns_multiline:
#        sequences = re.split(r'\s*\|\s*', pattern)  # Split the pattern into individual sequences.
#        sequences = [seq.strip().replace(' ', '').replace('\n', '') for seq in sequences]  # Trim whitespaces.
#        longest_seq = max(sequences, key=len)
#        
#        for seq in sequences:
#            print('\n')
#            print(seq)
#            if seq != longest_seq:
#                if not seq in longest_seq:
#                    raise InvalidMultisequenceException(seq)
#
#        # Replace the pattern with the longest sequence.
#        print('kkjjh')
#        print(pattern)
#
#        content_new = content_new.replace(full_expr, longest_seq)
#
#    patterns = re.findall(REGEX_MULTISEQUENCE, content_new, re.MULTILINE)
    
    patterns = re.findall(REGEX_MULTISEQUENCE, content_new, re.DOTALL)

    for pattern in patterns:
        sequences = pattern.split('|')  # Split the pattern into individual sequences.
        sequences = [seq.strip()[:-4] for seq in sequences]  # Trim whitespaces, and removes ".rna".
        longest_seq = max(sequences, key=len)

        for seq in sequences:
            if seq != longest_seq:
                if not seq in longest_seq:
                    raise InvalidMultisequenceException(seq)

        # Replace the pattern with the longest sequence.
        content_new = content_new.replace(pattern, longest_seq)

    return content_new


def replace_multisequence(match):
    for group in match.groups():
        if group:  # This check is to ignore None captures
            print(group)

def replace_produce(match_obj):
    rna_chain = match_obj.group(1)
    #dna_chain = rna_chain.replace('U', 'T')
    #return dna_chain
    return rna_chain

### Parser

class ParserCompiler():

    def __init__(self, target="DNA"):
        self.content = None
        self.target = target

    def parse(self, content):
        self.content = content
        self.content = re.sub(REGEX_SLIPPERY, replace_slippery_sequence, self.content)
        self.content = re.sub(r'\bproduce\b', '', self.content)
        self.content = re.sub(REGEX_RNA, replace_produce, self.content)
        self.content = re.sub(r'([AUGC]+)([\s\n]+)([AUGC]+)', r'\1\3', self.content)
        self.content = self.content.replace(' ', '')
        #self.content = capture_multisequences(self.content)

        if self.target == "DNA":
            # Remove the cap, the poly-A and replace the 'U' by the 'T'
            self.content = self.content.replace('U', 'T') 
            pass
        elif self.target == "RNA":
            # Nothing to do for now
            pass

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

def test_multisequence():
    text = """ prefix  AAAAAAUUUU.rna | AAAAA.rna | UUUU.rna | AAUU.rna suffix
    prefix GGCC.rna | GGCCGGCC.rna | GCCG.rna suffix """
    expected = ' prefix  AAAAAAUUUU.rna suffix\n    prefix GGCCGGCC.rna suffix ' 
    assert capture_multisequences(text) == expected

if __name__ == "__main__":
    test_multisequence()
