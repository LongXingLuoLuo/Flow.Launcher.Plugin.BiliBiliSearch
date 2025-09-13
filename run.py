import sys
from pathlib import Path

plugin_dir = Path.absolute(Path(__file__).parent)
paths = (".", "lib", "plugin")
sys.path = [str(plugin_dir / p) for p in paths] + sys.path

from plugin.main import BiliBiliSearchPlugin

if __name__ == '__main__':
    BiliBiliSearchPlugin()