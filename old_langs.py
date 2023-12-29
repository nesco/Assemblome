""" The lang module contains all the relevant code necessary to parse Assemblome files"""

# TO-DO
# * TEST
# * MIGRATE ALL "PROCESS_" in a single function of higher order which applies "replace_" to content

## Imports

import re

from utils import *
from utils_genomics import specify, translate
from langs.patterns import *
from langs.preprocessing import ParserPreprocessing

DB_UNIPROT = Uniprot()

## Functions

# Assembly

def replace_pdb_by_aa_chain(match):
    pdb_id = match.group(1)
    digit = match.group(2)

    if digit:  # if the optional digit part exists, remove the colon
        digit = int(digit[1])
    else:
        digit = 0

    return pdb_to_fasta_chains(pdb_id)[digit] + '.aa'

def replace_uniprot_by_aa_chain(match):
    uniprot_id = match.group(1)
    return DB_UNIPROT.get_sequence(uniprot_id) + '.aa'

def replace_id(s):
    output = re.sub(REGEX_PDB_CHAIN, replace_pdb_by_aa_chain, s)
    output = re.sub(REGEX_UNIPROT_CHAIN, replace_uniprot_by_aa_chain, output)
    return output

def parse_ids(content: list[str]) -> list[str]:
    return [replace_id(line) for line in content]

def replace_functional_expression(match_obj):
    """Replace functional expressions complement@amin-acid_chain and by Rna chains"""
    complement = match_obj.group(1)
    aa_chain = match_obj.group(2)

    if complement:
        #removing the "@" which is also captured by the capture group
        complement = complement[:-1]
    else:
        complement = ""

    rna_chain = specify(aa_chain, base64_to_list(complement)) + '.rna'
    return rna_chain


def process_functional_expression(s):
    return re.sub(REGEX_FUNCTIONAL_EXPRESSION, replace_functional_expression, s)

def parse_functional_expressions(content):
    return [process_functional_expression(line) for line in content]

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

def process_slippery_sequence(s):
    return re.sub(REGEX_SLIPPERY, replace_slippery_sequence, s)

def parse_slippery_sequence(content):
    content_new = [process_slippery_sequence(line) for line in content]
    return content_new

def replace_produce(match_obj):
    rna_chain = match_obj.group(1)
    dna_chain = rna_chain.replace('U', 'T')
    return dna_chain

def process_produce(s):
    return re.sub(REGEX_PRODUCE, replace_produce, s)

def parse_produce(content):
    content_new = [process_produce(line) for line in content]
    return content_new

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

