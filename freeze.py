from flask_frozen import Freezer
from recipyGui import recipyGui

freezer = Freezer(recipyGui)

if __name__ == '__main__':
    freezer.freeze()
