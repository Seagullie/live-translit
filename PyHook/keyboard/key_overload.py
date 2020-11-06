import pythoncom, pyWinhook as pyHook

class KeyOverloader:
    
    handle_injected = False
    
    def __init__(self):
        self.overload_map = {}
        
        hm = pyHook.HookManager()
        # watch for all mouse events
        hm.KeyDown = self.OnKeyboardEvent
        # set the hook
        hm.HookKeyboard()

    def OnKeyboardEvent(self, event): 
        if event.Injected and not self.handle_injected:
            return True
        
        should_suppress = False
        keys_pressed = ("Alt+" + event.Key) if event.Alt else event.Key
        
        if keys_pressed in self.overload_map:
            should_suppress = self.overload_map[keys_pressed]()
            
        return not bool(should_suppress) # cause if should_suppress is True, we need to return False
    
    def set_handler(self, key, handler):
        self.overload_map[key] = handler