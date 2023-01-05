""" Marker placement to the model
"""

import argparse
import logging

from metgem.default import default_model


def run():
    parser = argparse.ArgumentParser(description="List model", usage="metgem listmodel")
    for i, j in default_model.items():
        print("{} - {}".format(i, j))

    # TODO: Look into manifest
