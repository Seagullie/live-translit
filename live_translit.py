from keyboard import on_press, send, press, add_hotkey, on_press_key
from keyboard import write as Write
from playsound import playsound

from PyHook.export_ver.filter_mouse_clicks import LeftClickBlocker
from PyHook.keyboard.key_overload import KeyOverloader
from keylogger__f.keylogger import Keylogger
from translit_func.translit_func import Transliterator


class key_event:
    
    def __init__(self, name):
        self.name = name
        
        
space = key_event("space")
enter = key_event("enter")
EOF = key_event("EOF")

def send_erase_signal(n_of_signals):
    for _ in range(n_of_signals):
        send('backspace')

class LiveTransliterator: # shouldn't be used on it's own cause it references things from extended class
    input_lang = 'EN' 

    state = 1 # 1 - working. 0 - paused
    
    @staticmethod
    def write(text):
        return Write(text)
    
    def __init__(self):
        self.ukr_translit = Transliterator()
        self.key_logger = Keylogger()
        self.key_logger(standalone = False)
        self.click_handler = self.setup_click_blocker()
        self.overloader = KeyOverloader()
        self.handle_enter()
        self.handle_tab()
        self.handle_alt_tab()
        self.keybind_toggler()
    
    def setup_click_blocker(self):
        click_blocker = LeftClickBlocker()
        click_blocker.set_block_callback(lambda e: self.transliterate(EOF))
                
        return click_blocker
        
    def start_listening(self): 
        on_press(self.transliterate)
        self.click_handler.filter()
        
    def transliterate(self, key_event):
    
        if not self.state:
            return False
    
        last_key = key_event.name 
        if self.key_logger.memory:
            if last_key in self.wordenders:
                self.transliterate_and_edit_in(last_key)
                return True
            
        return False
    
    def transliterate_and_edit_in(self, last_key):
        transliterated_text = self.ukr_translit.transliterate(self.key_logger.memory_text)
        print(f"transliterated version to insert: {transliterated_text}. Original ver.: {self.key_logger.memory_text}")
        self.edit_textbox(last_key, transliterated_text)
            
    def edit_textbox(self, last_key, transliterated_text):
        self.erase_last_word(terminal_char = last_key)
        self.write(transliterated_text)
        send(last_key) if last_key not in self.special_symbols and last_key not in self.key_logger.keys_to_include else None
            
        self.key_logger.memory.clear()
            
    def erase_last_word(self, terminal_char):
        if self.ctrl_backspace():
            return
        
        last_word_len = len(self.key_logger.memory) + (1 if terminal_char not in self.special_symbols and terminal_char not in self.key_logger.keys_to_include else 0)     
        send_erase_signal(last_word_len)
            
    def ctrl_backspace(self):
        if "'" not in self.key_logger.memory and len(self.key_logger.memory) > 4:
            send("Ctrl+Backspace")
            return True
        return False
        
    def pause(self):
        print('transliterator has been paused')
        self.state = 0
        self.key_logger.pause()
        
        playsound('sounds/pause.wav', block = False)
        
    def cont(self):
        print('transliterator has been unpaused')
        self.state = 1
        self.key_logger.cont()
        
        playsound('sounds/cont.wav', block = False)
        
    def toggle_state(self):
        if self.state:
            self.pause()
        else:
            self.cont()
            
        return True # means 'should suppress'
        
    def keybind_toggler(self):
        self.overloader.set_handler(key = "Alt+T", handler = self.toggle_state)

    def handle_action_key(self, kb_event):
        if not self.state:
            send(kb_event.name)
        else:
            self.transliterate(kb_event)
    
    def handle_enter(self):
        self.overloader.set_handler(key = "Return", handler = lambda: self.transliterate(EOF))
        
    def handle_tab(self):   
        self.overloader.set_handler(key = "Tab", handler = lambda: self.transliterate(EOF))
        
    def handle_alt_tab(self):
        add_hotkey('Alt+Tab', lambda: self.key_logger.memory.clear, suppress = False) # the way to chain, i guess
        
    
class wordBasedTransliterator(LiveTransliterator):
    
    wordenders = [";", ":", "!", ")", "]", ",", ".", '"',
                  "}", ">", "?", "-", "_" ,"*", "space", "enter", "EOF"] 
    
    modifiers = ["ctrl", "alt"] 
    special_symbols = ["EOF", "enter"]
    noncontent_keys = modifiers + special_symbols
    
    wordenders_x_content_chars = ["enter"]
    
class granularTransliterator(wordBasedTransliterator):
    
    @staticmethod
    def write(text):
        return Write(text)
    
    def ctrl_backspace(self):
        return False
    
    def transliterate(self, key_event):
        
        if not self.state or super().transliterate(key_event):
            return False
        
        last_key = key_event.name.lower()
        
        if last_key in self.key_logger.keys_to_include:
            memory_text = self.key_logger.memory_text.lower()
            if not self.ukr_translit.is_part_of_combination(memory_text)\
                and not self.ukr_translit.ends_with_combo_init(memory_text):
                self.transliterate_and_edit_in(last_key)
                return True
            
        return False
            

live_transliterator = granularTransliterator()
live_transliterator.start_listening()

