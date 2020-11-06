import pyHook, pythoncom

def onMLD(event):
    print(f"click at {event.Position} registered")
    return True


hook_manager = pyHook.HookManager()
hook_manager.MouseLeftDown = onMLD

hook_manager.HookMouse()

pythoncom.PumpMessages()
