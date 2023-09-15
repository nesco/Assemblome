"""Utils Genomics module stores the helper functions which contains genomics knowledge"""

## Functions

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
