""" The lang module contains all the relevant code necessary to parse Assemblome files"""

######## Constants

# REGEXES to detect the main instructions of Assemblome 
# Import : 'import flsy as polypeptide'
# Tag: 'tag "FLSY.aa" as polypeptide'
# Functional expression: 'oKI@FLSY.aa'

REGEX_IMPORT =  r'^import (?P<path_import>[^"]+) as (?P<tag>\w+)$'
REGEX_TAG = r'^tag "(?P<data>[^"]+)" as (?P<tag>\w+)$'
REGEX_FUNCTIONAL_EXPRESSION = r'([A-Za-z0-9+/=]+)@([ARNDCQEGHILKMFPSTWYV]+)\.aa'
