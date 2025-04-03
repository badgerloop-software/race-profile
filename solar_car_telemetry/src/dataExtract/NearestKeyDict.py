class NearestKeyDict:
    def __init__(self, dictionary=None):
        self.data = {} if dictionary is None else dict(dictionary)
    
    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]
        
        if not self.data:
            raise KeyError(f"Dictionary is empty, can't find nearest key to {key}")
        
        # Find the key with the smallest absolute difference
        nearest_key = min(self.data.keys(), key=lambda k: abs(k - key))
        return self.data[nearest_key]
    
    def __setitem__(self, key, value):
        self.data[key] = value
    
    def __contains__(self, key):
        return key in self.data
    
    def __repr__(self):
        return f"NearestKeyDict({self.data})"