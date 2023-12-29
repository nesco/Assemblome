import re
import os
import sys


# from langs import parse_tags, parse_imports, parse_functional_expressions, parse_produce
from old_langs import *

def scan(path):
    """read a asb file and perform a lexical analysis."""
    
    instructions = ['#', 'import', 'tag', 'produce', 'raw']
    content = []
    
    #Read file
    with open(path, 'r') as file:
        content = list(map(str.strip, file))

    content = [line for line in content if not line.startswith("#") and not line == ""]
    #path_dir = '/'.join(patih.split('/')[:-1])
    #if len(path_dir) > 0:
    #    path_dir = path_dir + '/'
    #else:
    #    path_dir = './'
    #return content, path_dir
    return content

def parse(content, path):
    # TO-DO: get over this abomination
    preprocesser = ParserPreprocessing(path)
    content = preprocesser.parse(content)
    #return parse_produce(parse_slippery_sequence(parse_functional_expressions(parse_ids(parse_tags(parse_imports(content, path))))))
    return parse_produce(parse_slippery_sequence(parse_functional_expressions(parse_ids(content))))

def assemble(content, path):
    content_parsed = parse(content, path)
    content_linearized = ''.join(content_parsed)

    content_tabulated = ''
    for i, caracter in enumerate(content_linearized):
        if i % 70 == 0 and i > 0:
            content_tabulated += '\n'

        content_tabulated += caracter
    
    return content_tabulated

if __name__ == '__main__':
    
    if len(sys.argv) <= 2:
        print("Options:")
        print("-a / --assemble <path_to_file>: assemble an asb file")
        print("-d / --disassemble <path_to_file>: disassemble an FASTA file representing a DNA sequence")


    if len(sys.argv) > 2:
        # Retrieving the input file and its directory
        path_input = sys.argv[2]
        base_name = os.path.basename(path_input) 
        path = os.path.dirname(path_input)
        
        if len(path) > 0:
            path += "/"

        # -a option assemble an .asb file
        if sys.argv[1] in ["-a", "--assemble"]:

            content = scan(path_input)
            output = assemble(content, path)

            file_name, _ = os.path.splitext(base_name)

            with open(path + file_name + ".fna", 'w') as file:
                file.write(output)

        # To-Do: -d
        if sys.argv[1] in ["-d", "--disassemble"]:
            dna_chain = load_raw(path_input)
            rna_chain = dna_chain.replace('T', 'U')
            aa_chain, complement = translate(rna_chain)
            complement = list_to_base64(complement)
           
            (uniprot_id, entry_name) = DB_UNIPROT.sequence_to_id_and_entry_name[aa_chain] 
            print("UNIPROT ID: " + uniprot_id)
            print("Entry name: " + entry_name)
            print("Amino-acid sequence: " + aa_chain)
            print("Complement: " + complement)


    #content, path = scan('instruct_without_pdb.asb')
    #output = parse(content, path)
    #output_old = parse_functional_expressions(parse_tags(parse_imports(content, path)))
