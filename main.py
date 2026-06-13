import tkinter as tk
import win32gui
import win32con
import win32api
import keyboard
import os
import psutil


def exit_program():
    root.destroy()
    os._exit(0)

def update_stats():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().used / (1024 ** 3)
    
    label.config(text=f"CPU: {cpu}% | RAM: {ram:.2f}GB")
    
    root.after(1000, update_stats)

root = tk.Tk()

root.config(bg='white')
root.attributes('-transparentcolor', 'white')
root.attributes('-topmost', True) 
root.overrideredirect(True)      

hwnd = win32gui.GetParent(root.winfo_id())
style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
style = style | win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

label = tk.Label(root, text="CPU: --% | RAM: --GB", font=("Consolas", 12), fg="cyan", bg="white")
label.pack()

keyboard.add_hotkey('ctrl+alt+q', exit_program)

root.after(1000,update_stats)
root.mainloop()

