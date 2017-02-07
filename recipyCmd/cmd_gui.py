import socket
import threading
import webbrowser

import click
from recipyCommon import config as recipy_config
from recipyCmd.recipycmd import pass_config
from recipyGui import recipyGui


@click.command('gui', short_help='Launch GUI in default browser.')
@click.option('--no-browser', is_flag=True,
              help="Start GUI app, but don't open a browser.")
@pass_config
def cmd(config, no_browser):
    """Start ReciPy GUI in default browser."""
    port = get_free_port()
    url = 'http://127.0.0.1:{}'.format(port)

    if not no_browser:
        # Give the application some time before it starts
        threading.Timer(1.25, lambda: webbrowser.open(url)).start()

    # Turn off reloading by setting debug = False (this also fixes starting the
    # application twice)
    recipyGui.run(debug=config.debug, port=port)


def get_free_port():
    port = None
    base_port = recipy_config.get_gui_port()
    for trial_port in range(base_port, base_port + 5):
        try:
            s = socket.socket()
            s.bind(('', trial_port))
            s.close()
            port = trial_port
            break
        except Exception:
            # port already bound
            # Please note that this also happens when the gui is run in
            # debug mode!
            pass
    if not port:
        # no free ports above, fall back to random
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
    return port
