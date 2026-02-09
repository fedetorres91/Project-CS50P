"""Entry point for wallet application."""
# 20/1 Export transaction history to csv file,(DONE) 
# #TODO and print to UI
# TODO unit tests

import logging
import matplotlib
matplotlib.set_loglevel("warning")
logging.getLogger('matplotlib').setLevel(logging.WARNING)

from src.cli import main

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nProgram exited.")
        exit(0)
