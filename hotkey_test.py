import keyboard

def on_hotkey():
    print("Hotkey pressed!")

# Listen for Ctrl+Space
keyboard.add_hotkey('ctrl+space', on_hotkey)

print("Press Ctrl+Space to trigger...")
keyboard.wait('esc')  # Press Esc to exit the program
