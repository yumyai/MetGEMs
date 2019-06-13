""" Marker placement to the model
"""

import cmnet.default

def run():
    parser = argparse.ArgumentParser(
              description="Place marker to model",
              usage="cmnet markp input.fasta taxa.tsv")

    #parser.add_argument("-i", type=argparse.FileType("r"), required=True, help='')
    parser.add_argument("-t", type=argparse.FileType("r"), required=True, help='OTU table')
    parser.add_argument("-m", type=argparse.FileType("r"), required=True, help='Map file')
    parser.add_argument("-o", type=argparse.FileType("w"), required=True, help='Output table')
    args = parser.parse_args()

