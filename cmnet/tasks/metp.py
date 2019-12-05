""" Document
"""

import argparse
import cmnet.default

def run():
    parser = argparse.ArgumentParser(
              description="Map normalize classified reads into functional",
              usage="cmnet metpred ")

    parser.add_argument("-i", type=argparse.FileType("r"), help="")
    parser.add_argument("-o", type=argparse.FileType("r"), help="")

    args = parser.parse_args()