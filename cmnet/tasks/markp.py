""" Marker placement to the model
"""

import argparse
import cmnet.default
import pandas as pd
import numpy as np

def run():
    parser = argparse.ArgumentParser(
              description="Calculate model's abundance from marker data",
              usage="cmnet markp input.fasta taxa.tsv")

    parser.add_argument("-i", "--otutab", type=argparse.FileType("r"),
                        required=True, help='OTU table')
    parser.add_argument("-t", "--taxtsv", type=argparse.FileType("r"), required=True,
                        help='Linage files')
    parser.add_argument("-m", "--model", type=argparse.FileType("r"), required=True,
                        help='Linage files')
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), required=True,
                        help='Output table')
    args = parser.parse_args()

    # Load table
    otutab = pd.read_csv(args.otutab)
    taxtab = pd.read_csv(args.taxtsv)
    print(args.otutab)

def _calculate():
    # Align index and convert
    pass
