from ctypes import windll

user32 = windll.user32

langs = {'0x409': 'EN',
         '0x419': 'RU',
         '0x422': 'UA'}

def get_input_lang():

    window = user32.GetForegroundWindow()
    t_id = user32.GetWindowThreadProcessId(window, 0)

    kb_layout_id = user32.GetKeyboardLayout(t_id)
    kb_lang_id = kb_layout_id & (2 ** 16 - 1)

    kb_lang_id__hex = hex(kb_lang_id)

    return langs[kb_lang_id__hex] if kb_lang_id__hex in langs else kb_lang_id__hex


