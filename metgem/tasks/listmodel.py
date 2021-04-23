""" Marker placement to the model
"""

import argparse
import logging

import metgem.default
from metgem.default import default_map, default_model


def run():
    parser = argparse.ArgumentParser(description="List model", usage="metgem listmodel")
    for i, j in default_model.items():
        print("{} - {}".format(i, j))

    # TODO: Look into manifest