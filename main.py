from tag import Tag
from relationship import Relationship


def parse_tag(parts):
    """Parse a line meant to define a tag"""

    try:
        tag_value = parts[1].strip('"')
        tag_alias = parts[3]
        return Tag(tag_alias, tag_value)
    except Exception as e: #Parsing error
        print('Error: Cannot parse tag in line: {}'.format(" ".join(parts)))
        print('- ', e)
        return None


def parse_relationship(parts, tags):
    """Parse a line meant to define a relationship"""

    try:
        source_name, target_name = parts[1].split('@')
        if source_name in tags:
            source_name = tags[source_name].getValue()

        if target_name in tags:
            target_name = tags[target_name].getValue()

        return Relationship(source_name, target_name)
    except Exception as e:
        #Parsing error?
        print(e)
        print('Error: Cannot parse relationship in line: {}'.format(" ".join(parts)))
        return None


def scan(path):
    """read a asb file and perform a lexical analysis."""
    
    instructions = ['tag', 'produce', 'raw']
    content = []
    # Placeholder lists to store tags and relationships
    tags = {}
    relationships = {}
    
    #Read file
    with open(path, 'r') as file:
        content = list(map(str.strip, file))
    
    #Line by line analysis
    for line in content:
        parts = line.split()

        if parts[0] == 'tag' and parts[2] == 'as':
            tag = parse_tag(parts)
            if tag:
                tags[tag.getAlias()] = tag

        elif parts[0] == 'produce':
            relationship = parse_relationship(parts, tags)
            if relationship and relationship.to_str() not in relationships:
                relationships[relationship.to_str()] = relationship

    return content, tags, relationships


if __name__ == '__main__':
    content, tags, relationships = scan('instruct.asb')

    # Print the parsed tags and relationships
    for tag in tags.values():
        print(tag)
    for rel in relationships.values():
        print(rel)
