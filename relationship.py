class Relationship:
    def __init__(self, source, target):
        self.source = source
        self.target = target
    
    def __str__(self):
        return f'Relationship({self.source} -> {self.target})'
    
    def to_str(self):
        return f'{self.source}@{self.target}'
