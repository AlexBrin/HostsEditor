import hostseditor.log as log
import hostseditor.color as color
from hostseditor.editor import Editor, VERSION
import sys

__version__ = VERSION
__all__ = ["log", "color", "Editor", "__version__"]

if __name__ == '__main__':
    app = Editor()

    while app.command:
        if app.exit:
            log.info("Bye")
            sys.exit(0)

        app.run()
