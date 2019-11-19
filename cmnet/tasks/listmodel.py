""" Marker placement to the model
"""

import argparse
import logging

import cmnet.default
from cmnet.default import default_map, default_model

def run():
    parser = argparse.ArgumentParser(
            description="List model",
            usage="cmnet listmodel")
    for i, j in default_model.items():
        print("{} - {}".format(i, j))
    
    # TODO: Look into manifest