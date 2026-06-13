import tkinter as tk
import win32gui
import win32con
import keyboard
import os
import psutil

is_window_visible = True

def exit_program():
    root.destroy()
    os._exit(0)

def toogle_window():
    global is_window_visible
    if is_window_visible:
        root.withdraw()
        is_window_visible = False
    else:
        root.deiconify()
        is_window_visible = True

last_net_io = psutil.net_io_counters()

def update_stats():
    global last_net_io
    
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().used / (1024 ** 3)
    ram_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('C:/').percent
    process_count = len(psutil.pids())
    
    current_net_io = psutil.net_io_counters()
    download_speed = (current_net_io.bytes_recv - last_net_io.bytes_recv) / (1024 * 1024)
    last_net_io = current_net_io

    color = "red" if (cpu > 80 or ram_percent > 80) else "cyan"
    
    text = f"CPU: {cpu}% | RAM: {ram:.2f}GB | DL: {download_speed:.2f} MB/s | DISK: {disk_usage}% | PROC: {process_count}"
    label.config(text=text, fg=color)
    
    root.after(1000, update_stats)

root = tk.Tk()
root.config(bg='white')
root.attributes('-transparentcolor', 'white')
root.attributes('-topmost', True) 
root.overrideredirect(True)      

hwnd = win32gui.GetParent(root.winfo_id())
style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
style |= win32con.WS_EX_TOOLWINDOW | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)

label = tk.Label(root, text="Loading...", font=("Consolas", 12), fg="cyan", bg="white")
label.pack()

keyboard.add_hotkey('ctrl+alt+q', exit_program)
keyboard.add_hotkey('ctrl+alt+h', toogle_window)

root.after(1000, update_stats)
root.mainloop()