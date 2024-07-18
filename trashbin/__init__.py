import os

VERSION = "0.1.0"
TRASHBIN = os.path.expanduser("~/.local/share/trashbin")
CACHEBIN = os.path.expanduser("~/.cache/trashbin")
METADATA = os.path.join(CACHEBIN, "metadata")
