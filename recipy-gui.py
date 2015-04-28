#!/usr/bin/env python
from recipyGui import recipyGui
import threading, webbrowser, socket

def get_free_port():
    s = socket.socket()
    s.bind(('', 0))
    port = s.getsockname()[1]
    s.close()
    return port

port = get_free_port()
url = "http://127.0.0.1:{0}".format(port)

# Give the application some time before it starts
threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

recipyGui.run(debug = True, port=port)
