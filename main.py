import re

#### Genomics utils

def specify(aa_chain, complement):
    # Define the codon table
    # START implicit here
    # Source: https://en.wikipedia.org/wiki/Codon_degeneracy
    codon_table = {
        'A': ['GCU', 'GCC', 'GCA', 'GCG'],                    # Ala
        'R': ['CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],      # Arg
        'N': ['AAU', 'AAC'],                                  # Asn
        'D': ['GAU', 'GAC'],                                  # Asp
        'B': ['AAU', 'AAC', 'GAU', 'GAC'],                    # Asn or Asp
        'C': ['UGU', 'UGC'],                                  # Cys
        'Q': ['CAA', 'CAG'],                                  # Gln
        'E': ['GAA', 'GAG'],                                  # Glu
        'Z': ['CAA', 'CAG', 'GAA', 'GAG'],                    # Gln or Glu
        'G': ['GGU', 'GGC', 'GGA', 'GGG'],                    # Gly
        'H': ['CAU', 'CAC'],                                  # His
        'I': ['AUU', 'AUC', 'AUA'],                           # Ile
        'L': ['UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'],      # Leu
        'K': ['AAA', 'AAG'],                                  # Lys
        'M': ['AUG'],                                         # Met
        'F': ['UUU', 'UUC'],                                  # Phe
        'P': ['CCU', 'CCC', 'CCA', 'CCG'],                    # Pro
        'S': ['UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'],      # Ser
        'T': ['ACU', 'ACC', 'ACA', 'ACG'],                    # Thr
        'W': ['UGG'],                                         # Trp
        'Y': ['UAU', 'UAC'],                                  # Tyr
        'V': ['GUU', 'GUC', 'GUA', 'GUG'],                    # Val
        ' ': ['UAA', 'UGA', 'UAG']                            # STOP
    }


    # Add the STOP codon
    if aa_chain[-1] != ' ':
      aa_chain += ' '

    # Check if the two input chains have the same length
    if len(aa_chain) != len(num_chain):
        raise ValueError("The amino acid chain and the number chain must have the same length.")

    # Initialize the RNA sequence with the start codon
    rna_sequence = 'AUG'

    # Go through each amino acid and pick the corresponding codon
    for i, aa in enumerate(aa_chain):
        num = num_chain[i]

         # Check if the number is valid for the given amino acid
        if num >= len(codon_table[aa]):
            raise ValueError(f"The number {num} is too large for the amino acid {aa}.")

        rna_sequence += codon_table[aa][num]

    return rna_sequence

#### Lang 
def scan(path):
    """read a asb file and perform a lexical analysis."""
    
    instructions = ['tag', 'produce', 'raw']
    content = []
    
    with open(path, 'r') as file:
        content = list(map(str.strip, file))
    
    return content



def find_tag_pattern(text):
    """detect tag patterns"""
    data, tag = None, None

    # Define the regular expression pattern
    pattern = r'^tag "(?P<data>[^"]+)" as (?P<tag>\w+)$'

    # Match the pattern in the text
    match = re.fullmatch(pattern, text)

    if match:
        data = match.group('data')
        tag = match.group('tag')
        
    return data, tag

def parse_tag(content):
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
