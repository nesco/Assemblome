""" Utils.py module is there to store the helper functions """

## Imports

import requests

## Functions

# File access
def load_raw(path_import):
    """Load a file while removing the formatting. Useful for .fna files"""
    with open(path_import, 'r') as file:
        content = ''.join(list(map(str.strip, file)))

    return content

# Conversion of a list of integers between 0 and 5 from and to Base64

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

# DB retrievals

def pdb_to_fasta_chains(pdb_id):
    """Returns the corresponding FASTA amino-acid chains given a Protein Data Bank (PDB) Protein ID"""
    url = f"https://www.rcsb.org/fasta/entry/{pdb_id}"
    
    try:
      response = requests.get(url)
      response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
      print ("HTTP Error:",errh)
      return None
    except requests.exceptions.ConnectionError as errc:
      print ("Error Connecting:",errc)
      return None

    chains = response.text.split('>')[1:]
    chains = [line.split('\n')[-2] for line in chains]

    return chains

## Tests

def test_pdb_to_fasta_chains():
    chain_6VXX = "MGILPSPGMPALLSLVSLLSVLLMGCVAETGTQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPSGAGSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDPPEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKGSGRENLYFQGGGGSGYIPEAPRDGQAYVRKDGEWVLLSTFLGHHHHHHHH"

    assert pdb_to_fasta_chains("6VXX")[0] == chain_6VXX

if __name__ == "__main__":
    test_pdb_to_fasta_chains()
    print("All tests passed!")
