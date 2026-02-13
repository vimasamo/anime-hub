import uvicorn
import multiprocessing
import webbrowser
import time
import os
import sys

# Specific fix for --windowed mode in PyInstaller
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')
if sys.stdin is None:
    sys.stdin = open(os.devnull, 'r')

from main import app

def start_server():
    # Disable colors as they cause issues in non-tty environments (like windowed .exe)
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info", use_colors=False)

if __name__ == "__main__":
    # On Windows calling this function is necessary.
    if sys.platform.startswith('win'):
        multiprocessing.freeze_support()

    # Start server in a separate process
    server_process = multiprocessing.Process(target=start_server)
    server_process.start()

    # Wait for server to start
    time.sleep(2)

    # Open browser
    webbrowser.open("http://127.0.0.1:8000")

    try:
        server_process.join()
    except KeyboardInterrupt:
        server_process.terminate()
        server_process.join()
