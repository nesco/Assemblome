class Tag:
    def __init__(self, alias, value):
        self.alias = alias
        self.value = value
        self.attributes = {}
    
    def __str__(self):
        return f'Tag(alias={self.alias}, value={self.value})'
    
    def getAlias(self):
        return self.alias

    def getValue(self):
        return self.value