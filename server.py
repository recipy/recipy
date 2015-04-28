#!/usr/bin/env python
from recipyGui import recipyGui
import random, threading, webbrowser

port = 5000 + random.randint(0, 999)
url = "http://127.0.0.1:{0}".format(port)

# Give the application some time before it starts
threading.Timer(1.25, lambda: webbrowser.open(url) ).start()

recipyGui.run(debug = True, port=port)
