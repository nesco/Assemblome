import re

### Info utils

def baseX_to_baseY(num_str, base_x, base_y):
    """Convert a number from base-x to base-y using string manipulation."""
    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
    char_to_int = {char: i for i, char in enumerate(chars)}

    num_base10 = 0
    for digit in num_str:
        num_base10 = num_base10 * base_x + char_to_int[digit]

    if num_base10 == 0:
        return "0"

    num_baseY = ""
    while num_base10 > 0:
        num_base10, remainder = divmod(num_base10, base_y)
        num_baseY = chars[remainder] + num_baseY

    return num_baseY

def list_to_base64(lst):
    """Convert a list of integers [0, 5] to a base-64 string."""
    # Add a sentinel value '6' to preserve leading zeros
    lst_with_sentinel = [6] + lst
    num_base7 = ''.join(map(str, lst_with_sentinel))
    return baseX_to_baseY(num_base7, 7, 64)

def base64_to_list(base64_str):
    """Convert a base-64 string to a list of integers [0, 5]."""
    num_base7 = baseX_to_baseY(base64_str, 64, 7)
    # Remove the sentinel value '6' to get the original list
    return [int(digit) for digit in num_base7[1:]]

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
    if len(aa_chain) != len(complement):
        raise ValueError("The amino acid chain and the complement must have the same length.")

    # Initialize the RNA sequence with the start codon
    rna_sequence = 'AUG'

    # Go through each amino acid and pick the corresponding codon
    for i, aa in enumerate(aa_chain):
        num = complement[i]

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

def replace_functional_expression(match_obj):
    complement = match_obj.group(1)
    aa_chain = match_obj.group(2)
    rna_chain = specify(aa_chain, base64_to_list(complement)) + '.rna'
    return rna_chain

def process_functional_expression(s):
    pattern = r'([A-Za-z0-9+/=]+)@([ARNDCQEGHILKMFPSTWYV]+)\.aa'
    return re.sub(pattern, replace_functional_expression, s)

def parse_functional_expressions(content):
    content_new = [process_functional_expression(line) for line in content]
    return content_new

def parse(content):
    return parse_functional_expressions(parse_tags(content))
