""" Utils.py module is there to store the helper functions """

## Imports

import requests
import json
import typing
import pickle

## Functions

# File access
def load_raw(path_import):
    """Load a file while removing the formatting. Useful for .fna files"""
    with open(path_import, 'r') as file:
        content = ''.join(list(map(str.strip, file)))

    return content

def load_fasta(filename):
    """Loading a FASTA Database into three dictionaries: id2seq, entry2seq and seq2id&entry. Mostly used to load the Uniprot DB"""
    with open(filename, 'r') as file:
        lines = file.readlines()

    id_to_sequence = {}
    entry_name_to_sequence = {}
    sequence_to_id_and_entry_name = {}

    sequence = ""
    uniprot_id = ""
    entry_name = ""

    for line in lines:
        line = line.strip()
        if line.startswith('>'):
            if uniprot_id and sequence:  # Save the previous entry
                id_to_sequence[uniprot_id] = sequence
                entry_name_to_sequence[entry_name] = sequence
                sequence_to_id_and_entry_name[sequence] = (uniprot_id, entry_name)

            # Extract Uniprot ID and Entry Name from the header
            uniprot_id = line.split('|')[1]
            entry_name = line.split('|')[2].split(' ')[0]
            sequence = ""
        else:
            sequence += line

    # Save the last entry
    if uniprot_id and sequence:
        id_to_sequence[uniprot_id] = sequence
        entry_name_to_sequence[entry_name] = sequence
        sequence_to_id_and_entry_name[sequence] = (uniprot_id, entry_name)

    return id_to_sequence, entry_name_to_sequence, sequence_to_id_and_entry_name

def get_sequence_by_id_or_entry_name(key, id_to_sequence, entry_name_to_sequence):
    return id_to_sequence.get(key) or entry_name_to_sequence.get(key)

def get_id_and_entry_name_by_sequence(sequence, sequence_to_id_and_entry_name):
    return sequence_to_id_and_entry_name.get(sequence)

def save_to_disk(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

def load_from_disk(filename):
    with open(filename, 'rb') as file:
        return pickle.load(file)

# Load the data
#id_to_sequence, entry_name_to_sequence, sequence_to_id_and_entry_name = load_fasta('path_to_your_fasta_file.fasta')

# Example usage
#print(get_sequence_by_id_or_entry_name('Q6GZX4', id_to_sequence, entry_name_to_sequence))
#print(get_id_and_entry_name_by_sequence('MAFSAEDVLKEYDRRRRMEALLLSLYYPNDRKLLDYKEWSPPRVQVECPKAPVEWNNPPS...', sequence_to_id_and_entry_name))


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

def uniprot_to_fasta_chain(uniprot_id):
    """Returns the corresponding FASTA amino-acid chains given a Protein Data Bank (PDB) Protein ID"""
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.fasta"
    
    try:
      response = requests.get(url)
      response.raise_for_status()
    except requests.exceptions.HTTPError as errh:
      print ("HTTP Error:",errh)
      return None
    except requests.exceptions.ConnectionError as errc:
      print ("Error Connecting:",errc)
      return None
    
    chain = response.text.split('>')[1]
    chain = ''.join(chain.split('\n')[1:])

    return chain

def protein_sequence_to_PDB_ID(protein_sequence: str):
    """Given the FASTA Amino-Acid chain of a given protein, returns the most probable PDB ID"""

    # Define the URL for the search
    url = "https://www.rcsb.org/search/data"

    # Define the JSON payload
    data = {
        "report": "pdb_ids",
        "request": {
            "query": {
                "type": "group",
                "logical_operator": "and",
                "nodes": [{
                    "type": "terminal",
                    "service": "sequence",
                    "parameters": {
                        "evalue_cutoff": 0.1,
                        "identity_cutoff": 0,
                        "sequence_type": "protein",
                        "value": protein_sequence  # Insert the protein sequence here
                    }
                }]
            },
            "return_type": "entry",
            "request_options": {
                "paginate": {
                    "start": 0,
                    "rows": 25
                },
                "results_content_type": ["experimental"],
                "sort": [{
                    "sort_by": "score",
                    "direction": "desc"
                }],
                "scoring_strategy": "combined"
            }
        },
        "getDrilldown": False,
        "attributes": None
    }

    # Make the POST request
    response = requests.post(url, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response to extract PDB IDs or any other relevant information
        response_data = response.json()
        pdb_ids = response_data.get('result_set', [])
        
        if len(pdb_ids) > 0:
            pdb_id = pdb_ids[0]
            print(pdb_id)
            print(pdb_to_fasta_chains(pdb_id))
    else:
        print("Error:", response.status_code)

## Class

class Uniprot():
    """Object to encapsulate access to the uniprot DB data. Act as a blackbox on the pickle cache system"""
    

    def __init__(self):
        self.id_to_sequence = {}
        self.entry_name_to_sequence = {}
        self.sequence_to_id_and_entry_name = {}
        try:
            self.id_to_sequence = load_from_disk('./data/id_to_sequence.pkl')
            self.entry_name_to_sequence = load_from_disk('./data/entry_name_to_sequence.pkl')
            self.sequence_to_id_and_entry_name = load_from_disk('./data/sequence_to_id_and_entry_name.pkl')
        except (FileNotFoundError, pickle.UnpicklingError):
            self.id_to_sequence, self.entry_name_to_sequence, self.sequence_to_id_and_entry_name = load_fasta('./data/uniprot_sprot.fasta')
            save_to_disk(self.id_to_sequence, './data/id_to_sequence.pkl')
            save_to_disk(self.entry_name_to_sequence, './data/entry_name_to_sequence.pkl')
            save_to_disk(self.sequence_to_id_and_entry_name, './data/sequence_to_id_and_entry_name.pkl')

    def get_sequence(self, identifier):
        return get_sequence_by_id_or_entry_name(identifier, self.id_to_sequence, self.entry_name_to_sequence)

    def get_identifiers(self, sequence):
        return get_id_and_entry_name_by_sequence(sequence, self.sequence_to_id_and_entry_name)
            

## Tests

def test_pdb_to_fasta_chains():
    chain_6VXX = "MGILPSPGMPALLSLVSLLSVLLMGCVAETGTQCVNLTTRTQLPPAYTNSFTRGVYYPDKVFRSSVLHSTQDLFLPFFSNVTWFHAIHVSGTNGTKRFDNPVLPFNDGVYFASTEKSNIIRGWIFGTTLDSKTQSLLIVNNATNVVIKVCEFQFCNDPFLGVYYHKNNKSWMESEFRVYSSANNCTFEYVSQPFLMDLEGKQGNFKNLREFVFKNIDGYFKIYSKHTPINLVRDLPQGFSALEPLVDLPIGINITRFQTLLALHRSYLTPGDSSSGWTAGAAAYYVGYLQPRTFLLKYNENGTITDAVDCALDPLSETKCTLKSFTVEKGIYQTSNFRVQPTESIVRFPNITNLCPFGEVFNATRFASVYAWNRKRISNCVADYSVLYNSASFSTFKCYGVSPTKLNDLCFTNVYADSFVIRGDEVRQIAPGQTGKIADYNYKLPDDFTGCVIAWNSNNLDSKVGGNYNYLYRLFRKSNLKPFERDISTEIYQAGSTPCNGVEGFNCYFPLQSYGFQPTNGVGYQPYRVVVLSFELLHAPATVCGPKKSTNLVKNKCVNFNFNGLTGTGVLTESNKKFLPFQQFGRDIADTTDAVRDPQTLEILDITPCSFGGVSVITPGTNTSNQVAVLYQDVNCTEVPVAIHADQLTPTWRVYSTGSNVFQTRAGCLIGAEHVNNSYECDIPIGAGICASYQTQTNSPSGAGSVASQSIIAYTMSLGAENSVAYSNNSIAIPTNFTISVTTEILPVSMTKTSVDCTMYICGDSTECSNLLLQYGSFCTQLNRALTGIAVEQDKNTQEVFAQVKQIYKTPPIKDFGGFNFSQILPDPSKPSKRSFIEDLLFNKVTLADAGFIKQYGDCLGDIAARDLICAQKFNGLTVLPPLLTDEMIAQYTSALLAGTITSGWTFGAGAALQIPFAMQMAYRFNGIGVTQNVLYENQKLIANQFNSAIGKIQDSLSSTASALGKLQDVVNQNAQALNTLVKQLSSNFGAISSVLNDILSRLDPPEAEVQIDRLITGRLQSLQTYVTQQLIRAAEIRASANLAATKMSECVLGQSKRVDFCGKGYHLMSFPQSAPHGVVFLHVTYVPAQEKNFTTAPAICHDGKAHFPREGVFVSNGTHWFVTQRNFYEPQIITTDNTFVSGNCDVVIGIVNNTVYDPLQPELDSFKEELDKYFKNHTSPDVDLGDISGINASVVNIQKEIDRLNEVAKNLNESLIDLQELGKYEQYIKGSGRENLYFQGGGGSGYIPEAPRDGQAYVRKDGEWVLLSTFLGHHHHHHHH"

    assert pdb_to_fasta_chains("6VXX")[0] == chain_6VXX

# if __name__ == "__main__":
#     test_pdb_to_fasta_chains()
#     print("All tests passed!")
