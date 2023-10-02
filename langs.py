""" The lang module contains all the relevant code necessary to parse Assemblome files"""

## Imports

import re

from utils import list_to_base64, base64_to_list, pdb_to_fasta_chains, uniprot_to_fasta_chain, load_raw, protein_sequence_to_PDB_ID
from utils_genomics import specify, translate

## Constants

# REGEXES to detect the main instructions of Assemblome 
# Import : 'import flsy as polypeptide'
# Tag: 'tag "FLSY.aa" as polypeptide'
# Functional expression: 'oKI@FLSY.aa'

REGEX_IMPORT =  r'^import (?P<data>[^"]+) as (?P<tag>\w+)$'
REGEX_TAG = r'^tag "(?P<data>[^"]+)" as (?P<tag>\w+)$'
REGEX_FUNCTIONAL_EXPRESSION = r'([A-Za-z0-9+/=]+@)?([ARNDCQEGHILKMFPSTWYV]+)\.aa'
REGEX_PRODUCE = r'^produce ([AUGC]+)\.rna'
REGEX_RNA = r'([AUGC]+)\.rna'

# PDB and Uniprot
# Either 'PCHS.pdb'
# Or 'from PDB import PCHS as random_protein' (equivalent to a tag PCHS.pdb as random_protein)
REGEX_PDB_CHAIN = r'(?P<id_pdb>[A-Z0-9]{4})(?P<chain>:\d)?\.pdb'
REGEX_UNIPROT_CHAIN = r'(?P<id_uniprot>[A-Z0-9]{6-11})\.up'

## Functions

# Assembly

def find_replacement_pattern(text, regex):
    """Detect patterns which are used to replace a given token by some other data."""
    data, tag = None, None

    # Match the pattern in the text
    match = re.fullmatch(regex, text)

    if match:
        data = match.group('data')
        tag = match.group('tag')

    return data, tag

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

def parse_imports(content, path_current):
    """replace all tags by their corresponding data following the tag instructions"""
    return inverse_progressive_replacement(content, REGEX_IMPORT, lambda path: load_raw(path_current + path))

def parse_tags(content):
    """replace all tags by their corresponding data following the tag instructions"""
    return inverse_progressive_replacement(content, REGEX_TAG, lambda x: x)

def replace_pdb_by_aa_chain(match):
    pdb_id = match.group(1)
    digit = match.group(2)

    if digit:  # If the optional digit part exists, remove the colon
        digit = int(digit[1])
    else:
        digit = 0

    return pdb_to_fasta_chains(pdb_id)[digit] + '.aa'

def replace_uniprot_by_aa_chain(match):
    uniprot_id = match.group(1)

    return uniprot_to_fasta_chain(uniprot_id) + '.aa'

def replace_id(s):
    output = re.sub(REGEX_PDB_CHAIN, replace_pdb_by_aa_chain, s)
    output = re.sub(REGEX_UNIPROT_CHAIN, replace_uniprot_by_aa_chain, output)

    return output

def parse_ids(content):
    return [replace_id(line) for line in content]

def replace_functional_expression(match_obj):
    complement = match_obj.group(1)
    aa_chain = match_obj.group(2)

    if complement:
        complement = complement[:-1]
    else:
        complement = ""

    rna_chain = specify(aa_chain, base64_to_list(complement)) + '.rna'
    return rna_chain

def process_functional_expression(s):
    return re.sub(REGEX_FUNCTIONAL_EXPRESSION, replace_functional_expression, s)

def parse_functional_expressions(content):
    return [process_functional_expression(line) for line in content]

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
def rna_to_functional_expression(rna_chain):
    aa_chain, complement = translate(rna_chain)
    return list_to_base64(complement) + "@" + aa_chain + ".aa"

def replace_rna_by_functional_expression(s):
    return re.sub(REGEX_RNA, lambda match: rna_to_functional_expression(match.group(1)), s)
