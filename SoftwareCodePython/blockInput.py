#coding: utf-8
#developer: Deiner Zapata Silva

#Bloquear el ingreso de datos del usuario por teclado y ratón.
#pip install keyboard
#pip install mouse

#pip install pyHook
#pip install pygame


import pyHook

# create a keyboard hook
def OnKeyboardEvent(event):
    print("MessageName:"+str(event.MessageName))
    if(event.Key.lower() in ['lwin', 'tab', 'lmenu'])
        return False
    else:
        return True
# create a hook manager
hm = pyHook.HookManager()
#watch for all keyboard events
hm.KeyDown = OnKeyboardEvent
hm.HookKeyboard()

print("teclas captadas......") 