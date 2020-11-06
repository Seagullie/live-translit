import re
from .translit_tables.tables import ua 

def replace_keep_case(word, replacement, text):
    
    def func(match):
        g = match.group()
        if g.islower(): return replacement.lower()
        if g.istitle(): return replacement.title()
        if g.isupper(): return replacement.upper()
        return replacement  
        
    return re.sub(word, func, text, flags=re.I)

def is_nonASCII(text):
    for char in text:
        if char.isascii():
            return False
        
    return True

class Transliterator:
    
    replacement_map = ua
    
    postreplacement_map = {
        "̚̚̚̚ϟ": "'"
    }
    
    def __init__(self):
        self.keys = sorted(self.replacement_map, key = len, reverse = True)
        self.combos = list(filter(lambda k: len(k) > 1, self.keys))
    
    def transliterate(self, text):
        for key in self.keys:
            text = replace_keep_case(key, self.replacement_map[key], text)
            
            if is_nonASCII(text):
                break
                
        return self.postprocess(text)
    
    def postprocess(self, text):
        for char in self.postreplacement_map:
            text = text.replace(char, self.postreplacement_map[char])
            
        return text
    
    def is_part_of_combination(self, text):
        for combo in self.combos:
            if len(combo) > len(text) and combo.startswith(text):
                return True
            
        return False
    
    def ends_with_combo_init(self, text):
        return self.is_part_of_combination(text[-1])