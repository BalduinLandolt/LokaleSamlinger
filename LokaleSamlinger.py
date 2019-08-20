"""
By Balduin Landolt

See Github for more info.

Run with exactly one command line parameter, that refers to the
Entry on Digitale Samlinger, (e.g. `7465`).
"""

import sys

def run_harvester(entry_id):
    print("Looking for: {}".format(entry_id))
    # TODO: Do stuff.


if __name__ == "__main__":
    print("Running...")
    print("Number of Arguments: {}".format(len(sys.argv)))
    print("Arguments: {}".format(sys.argv))
    if len(sys.argv) != 2:
        print("Unexpected number of arguments.\nAbort.")
        exit(-1)
    run_harvester(sys.argv[1])
    print("Done.")
