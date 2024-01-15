"""This module contains the parser that translate every non nucleotide sequences into sequences of nucleotides.
Once used, all the information remaining should be directly expressed in terms of nucleotides. It means there should not be any longer references to amino-acids, complements, and databases"""

### Imports
import re
from utils import *
from utils_genomics import specify, translate

### Databases
DB_UNIPROT = Uniprot()

### Patterns

REGEX_FUNCTIONAL_EXPRESSION = r'([A-Za-z0-9+\/=]+@)?([ARNDCQEGHILKMFPSTWYV]+)\.aa'

# PDB and Uniprot
# Either 'PCHS.pdb'
# Or 'from PDB import PCHS as random_protein' (equivalent to a tag PCHS.pdb as random_protein)
REGEX_PDB_CHAIN = r'(?P<id_pdb>[A-Z0-9]{4})(?P<chain>:\d)?\.pdb'
REGEX_UNIPROT_CHAIN = r'(?P<id_uniprot>[A-Z0-9]{6,11})\.up'

REGEX_UNIPROT_IMPORT = r'Uniprot\["?(?P<id_uniprot>[A-Z0-9]{6,11})"?\]'

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


### Parser

class ParserConverter():
    
    def __init__(self):
        self.content = None

    def parse(self, content):
        self.content = content

        # parse database identifiers
        self.content = re.sub(REGEX_PDB_CHAIN, replace_pdb_by_aa_chain, self.content)
        self.content = re.sub(REGEX_UNIPROT_CHAIN, replace_uniprot_by_aa_chain, self.content)

        self.content = re.sub(REGEX_UNIPROT_IMPORT, lambda match: DB_UNIPROT.get_sequence(match.group(1)) + ".aa", self.content)

        # parse functional expressions
        self.content = re.sub(REGEX_FUNCTIONAL_EXPRESSION, replace_functional_expression, self.content)

        return self.content

### Tests

def test_parser():
    text = """
    I am singiiiiing oKI@FLSY.aa in the rain, I am oKI@FLSY.aa singining in the raiiiin!
    Oh oKI@FLSY.aa mamy bluuuue
    """
    parsed = converter.parse(text)
    expected = "\nI am singiiiiing AUGUUUUUGUCAUACUAG.rna in the rain, I am AUGUUUUUGUCAUACUAG.rna singining in the raiiiin!\n    Oh AUGUUUUUGUCAUACUAG.rna mamy bluuuue\n    "
    assert parsed == expected

def test_uniprot_retrieval():
    # Test strings
    test_strings = [
        'Uniprot["P123456"]',
        'Uniprot[P123456]',
        'Uniprot["ABCDEFG"]',
        'Some other string',
        'Uniprot["12345678901"]',  # Longer than 11 characters
        'Uniprot[P1234"]'          # Mismatched quotes
    ]

    # Test the regex on each string
    for test_string in test_strings:
        match = re.search(REGEX_UNIPROT_IMPORT, test_string)
        if match:
            print(f"Matched: {test_string} - ID: {match.group('id_uniprot')}")
        else:
            print(f"Did not match: {test_string}")

    text = 'hi guys! Uniprot["P0DTC2"] '
    text = re.sub(REGEX_UNIPROT_IMPORT, lambda m: m.group(1), text)
    print(text)
