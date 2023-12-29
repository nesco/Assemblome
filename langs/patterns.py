""" This module is used to store all the Regexes required to parse Assemblome files."""

# REGEXES to detect the main instructions of Assemblome 
# Import : 'import flsy as polypeptide'
# Tag: 'tag "FLSY.aa" as polypeptide'
# Functional expression: 'oKI@FLSY.aa'

REGEX_FUNCTIONAL_EXPRESSION = r'([A-Za-z0-9+\/=]+@)?([ARNDCQEGHILKMFPSTWYV]+)\.aa'
REGEX_SLIPPERY = r'([AUGC]+)\.rna\s+(<+|>+)\s+([AUGC]+)\.rna'
REGEX_PRODUCE = r'^produce ([AUGC]+)\.rna'
#REGEX_RNA = r'([AUGC]+)\.rna'

# PDB and Uniprot
# Either 'PCHS.pdb'
# Or 'from PDB import PCHS as random_protein' (equivalent to a tag PCHS.pdb as random_protein)
REGEX_PDB_CHAIN = r'(?P<id_pdb>[A-Z0-9]{4})(?P<chain>:\d)?\.pdb'
REGEX_UNIPROT_CHAIN = r'(?P<id_uniprot>[A-Z0-9]{6,11})\.up'
