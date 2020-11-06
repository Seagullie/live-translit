from keyboard import on_press, is_pressed, is_modifier, wait

from .detect_current_input_language.get_current_input_lang import get_input_lang

modifiers = ['ctrl', 'alt', 'windows', 'shift']
alphabet = "abcdefghijklmnopqrstuvwxyz"

def is_combo_pressed():
    pass

def is_modifier_pressed():
    for mod in modifiers:
        if is_pressed(mod):
            return True
    
    return False

class Keylogger:
    
    lang = 'EN'
    keys_to_include = alphabet + "'"
    
    state = 1 # 1 - working. 0 - paused
    
    def __init__(self):
        self.memory = []
    
    memory_text = property(lambda self: "".join(self.memory))
    
    def __call__(self, standalone = True):
        on_press(callback = self.log_key)
        if standalone:
            wait()
    
    def log_key(self, e):
        
        if not self.state:
            return
        
        key_name = e.name.lower()
        
        if key_name == 'backspace':
            return self.handle_backspace()
    
        if self.should_clear_memory(key_name):
            return self.memory.clear()
    
        if self.should_discard_key(key_name):
            return
        
        if is_pressed('shift'):
            key_name = key_name.upper()
            
        self.memory.append(key_name)
        
    def should_discard_key(self, key_name):
        if get_input_lang() != self.lang:
            return True
        
        if key_name not in self.keys_to_include:
            return True
        
        if not is_pressed('shift'):
            if is_modifier_pressed():
                return True
            
    def should_clear_memory(self, key_name):
        if key_name == 'tab' and is_pressed('alt'):
            return True
        
    def handle_backspace(self):
        if not self.memory:
            return
        
        if is_pressed('ctrl'):
            while self.memory and self.memory[-1] != "'":
                self.memory.pop()
        else:
            self.memory.pop()
            
    def pause(self):
        self.state = 0
        self.memory.clear()
        
    def cont(self):
        self.state = 1
