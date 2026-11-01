import sqlite3
import time
from datetime import datetime
import threading
import os
import tkinter as tk
import pyperclip
import keyboard

# --- HIGH DPI AWARENESS FOR WINDOWS (Fix blurry UI on 4K/HiDPI screens) ---
try:
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass

# Define base directory and SQLite database path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "clipboard_history.db")
MAX_ITEMS = 300  # Maximum number of clipboard items to keep in history

def init_db():
    """Initialize the SQLite database and create the table if it doesn't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clipboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_str TEXT NOT NULL,
            time_str TEXT NOT NULL,
            content TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def cleanup_old_items():
    """Keep only the latest MAX_ITEMS records and delete older entries."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM clipboard 
        WHERE id NOT IN (
            SELECT id FROM clipboard ORDER BY id DESC LIMIT ?
        )
    ''', (MAX_ITEMS,))
    conn.commit()
    conn.close()

def save_to_db(content):
    """Save new clipboard text to the database, avoiding consecutive duplicates."""
    if not content or not content.strip():
        return
        
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Check if the content is identical to the most recent entry today
    cursor.execute('''
        SELECT content FROM clipboard 
        WHERE date_str = ? ORDER BY id DESC LIMIT 1
    ''', (date_str,))
    last_row = cursor.fetchone()
    
    if not last_row or last_row[0] != content:
        cursor.execute('''
            INSERT INTO clipboard (date_str, time_str, content)
            VALUES (?, ?, ?)
        ''', (date_str, time_str, content))
        conn.commit()
        cleanup_old_items()
        
    conn.close()

def show_clipboard_ui():
    """Display the Tkinter search-enabled clipboard history popup window."""
    root = tk.Tk()
    root.title("Python Clipboard Manager (Win + V)")
    root.geometry("700x520")

    # --- ADD WINDOW ICON ---
    try:
        icon_path = os.path.join(BASE_DIR, "icon.ico")
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
    except Exception:
        pass

    # --- SEARCH BAR FRAME ---
    search_frame = tk.Frame(root)
    search_frame.pack(fill=tk.X, padx=12, pady=12)

    lbl_search = tk.Label(search_frame, text="🔍 Search:", font=("Segoe UI", 10, "bold"))
    lbl_search.pack(side=tk.LEFT, padx=(0, 8))

    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Segoe UI", 11))
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    search_entry.focus()

    # --- HISTORY LISTBOX FRAME ---
    list_frame = tk.Frame(root)
    list_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 10))

    scrollbar = tk.Scrollbar(list_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Consolas", 10))
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    # Fetch all clipboard history from SQLite
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, date_str, time_str, content FROM clipboard ORDER BY id DESC')
    all_rows = cursor.fetchall()
    conn.close()

    item_map = {}

    def populate_list(filter_text=""):
        """Populate the listbox with records, filtered by search query."""
        listbox.delete(0, tk.END)
        item_map.clear()
        
        display_idx = 0
        for row in all_rows:
            item_id, d_str, t_str, content = row
            if filter_text.lower() in content.lower() or filter_text.lower() in d_str.lower():
                preview = content.replace("\n", " ")[:95]
                display_text = f"[{d_str} {t_str}] {preview}"
                listbox.insert(tk.END, display_text)
                item_map[display_idx] = content
                display_idx += 1

    populate_list()

    def on_search_changed(*args):
        """Real-time filter callback when typing in the search bar."""
        populate_list(search_var.get())

    search_var.trace_add("write", on_search_changed)

    def on_select(event):
        """Copy selected item back to clipboard and close the UI window."""
        selection = listbox.curselection()
        if selection:
            idx = selection[0]
            selected_content = item_map.get(idx)
            if selected_content:
                pyperclip.copy(selected_content)
                root.destroy()

    listbox.bind('<Double-Button-1>', on_select)
    listbox.bind('<Return>', on_select)

    # Info footer label
    lbl_info = tk.Label(root, text="💡 Enter keywords to search • Double-click or Enter to copy the text.", fg="gray", font=("Segoe UI", 9))
    lbl_info.pack(pady=8)

    root.mainloop()

def monitor_clipboard():
    """Background loop to continuously monitor clipboard changes."""
    last_clipboard = ""
    while True:
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard != last_clipboard:
                last_clipboard = current_clipboard
                save_to_db(current_clipboard)
        except Exception:
            pass
        time.sleep(1)

if __name__ == "__main__":
    init_db()
    
    # Register global hotkey to override Win + V and trigger UI
    keyboard.add_hotkey('windows+v', lambda: threading.Thread(target=show_clipboard_ui, daemon=True).start(), suppress=True)

    # Start clipboard background monitoring thread
    t = threading.Thread(target=monitor_clipboard, daemon=True)
    t.start()

    # Keep script running in the background
    keyboard.wait()