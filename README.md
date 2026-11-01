**# Python Windows Clipboard Manager (`Win + V`)**



A lightweight, open-source clipboard manager for \*\*Windows 11\*\* built with Python. It replaces the default Windows clipboard history limit (25 items) with an expandable, searchable local database supporting up to \*\*300 items\*\* organized by date and time.



\---



**## ✨ Features**



\- \*\*Expanded History:\*\* Keeps up to 300 recent clipboard items in a lightweight local SQLite database.

\- \*\*Real-time Search Bar:\*\* Instantly filter your past copied clips by keywords or dates.

\- \*\*Global Hotkey (`Win + V`):\*\* Overrides and replaces the default Windows clipboard shortcut seamlessly.

\- \*\*High DPI Support:\*\* Fully optimized for high-resolution screens (4K/HiDPI) on Windows 11.

\- \*\*Runs Silently:\*\* Background execution using `.pyw` extension without displaying a persistent console window.



\---



**## 🛠️ Prerequisites \& Installation**



1\. Make sure \*\*Python\*\* is installed on your Windows system.

2\. Clone or download this repository into a dedicated folder (e.g., `Documents\\ClipboardManager`).

3\. Install the required Python packages via Command Prompt (CMD):

&#x20;  ```bash

&#x20;  pip install pyperclip keyboard

🚀 How to Run \& Setup Startup

**1. Manual Run**

Rename or save the main script as clipboard\_manager\_pro.pyw.



Double-click the file to start it in the background. Press Win + V anytime to open the management panel.



**2. Run Automatically on Windows Startup**

To make the tool start automatically every time you turn on your PC:



Press Win + R, type shell:startup, and press Enter.



Right-click clipboard\_manager\_pro.pyw -> Show more options -> Create shortcut.



Move or paste that shortcut directly into the opened Startup folder.



📂 Project Structure



📦 ClipboardManager/

&#x20;┣ 📜 clipboard\_manager\_pro.pyw  # Main background script \& UI

&#x20;┣ 📜 icon.ico                   # Application custom icon (optional)

&#x20;┗ 🗄️ clipboard\_history.db       # Auto-generated SQLite local database



💡 Usage Tips

To Search: Press Win + V, type any keyword into the search box to filter instantly.



To Copy an Item: Double-click the item or highlight it and press Enter. The text will be instantly copied back to your active clipboard.



To Quit: Open Task Manager (Ctrl + Shift + Esc), find the running Python process, and click End task.



📝 License

This project is open-source and available under the MIT License.

