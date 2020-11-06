import pyWinhook as pyHook, pythoncom

class LeftClickBlocker:
    
    def __init__(self):
        self.hook_manager = hook_manager = pyHook.HookManager()
        hook_manager.MouseLeftDown = self.on_mouse_left_down
        
        self.block_condition = lambda: True
        
    def set_block_condition(self, func):
        self.block_condition = func
    
    def set_block_callback(self, callback):
        self.block_callback = callback
    
    def on_mouse_left_down(self, e):
        
        if self.block_condition():
            self.block_callback(e)
            
        return True
    
    def filter(self):
        self.hook_manager.HookMouse()
        pythoncom.PumpMessages() # blocks the thread
