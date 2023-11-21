""" Store the function to translate DNA sequences to a ASB file """

def create_alternative_sequences(dna_strand):
    """ For a DNA strand, create the three possible reading by croping the first and the second letters"""
    readings = [dna_strand, dna_strand[1:], dna_strand[2:]]
    return readings

def decompose_into_codons(dna_sequence):
    # Ensure the DNA sequence length is a multiple of 3
    trimmed_length = len(dna_sequence) - (len(dna_sequence) % 3)
    trimmed_sequence = dna_sequence[:trimmed_length]
    
    # Decompose the sequence into codons
    codons = [trimmed_sequence[i:i+3] for i in range(0, trimmed_length, 3)]
    
    return codons

def split_at_stop_codons(codons):
    stop_codons = {'TAA', 'TAG', 'TGA'}
    proteins = []
    current_protein = []

    for codon in codons:
        if codon in stop_codons:
            if current_protein:  # if there is something in the current protein list
                proteins.append(current_protein)
                current_protein = []
            # If you want to include stop codons in the resulting lists, uncomment the next line
            # current_protein.append(codon)
        else:
            current_protein.append(codon)

    # Add the last protein if it ends without a stop codon
    if current_protein:
        proteins.append(current_protein)

    return proteins

# Example usage:
#dna_seq = "ATGCGAATGCGTAGCTAATAGCTAATCGTGA"
#codons = decompose_into_codons(dna_seq)
#proteins = split_at_stop_codons(codons)
#for i, protein in enumerate(proteins, start=1):
#    print(f"Protein {i}: {protein}")
    
# Example usage:
#dna_seq = "ATGCGAATGCGTAGCTAGCTAATCG"
#codons = decompose_into_codons(dna_seq)
#print("Codons:", codons)
