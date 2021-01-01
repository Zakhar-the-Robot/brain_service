import sys
import os

try:
    SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
    sys.path.append(SCRIPT_PATH + "/../python_packages")
    from service_display import start
except ImportError:
    raise ImportError("Cannot find service_display")

if __name__ == "__main__":
    start()
