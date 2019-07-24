""" Regroup reaction into KO or EC
"""

import argparse
from pandas import DataFrame
import numpy as np
import cmnet.default
from cmnet.default import default_map
from cmnet.utils import read_grouper, _align_dataframe
import pandas as pd

def run():
    parser = argparse.ArgumentParser(
            description="Calculate model's abundance from marker data",
            usage="cmnet markp -i input.fasta -t taxa.tsv -m [genus/species] -o output.tsv")

    parser.add_argument("-i", "--input", type=argparse.FileType("r"),
                        required=True, help='Reaction table')
    parser.add_argument("-g", "--group", type=str,
                        required=True, help='{ec, ko}')
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), required=True,
                        help='File name for output table')
    args = parser.parse_args()
    
    # Load input
    functiontab = pd.read_csv(args.input, sep="\t", header=0, index_col=0)

    # Load table
    if args.group not in ["ec", "ko"]:
        raise ValueError()

    f2g = read_grouper(default_map[args.group.upper()])
    samplegroup = function2group(functiontab, f2g)
    # round number
    samplegroup = samplegroup.round(5)
    samplegroup.to_csv(args.output, sep="\t")


def function2group(reaction_tab, f2gtab) -> DataFrame:
    """ Group reactions into other functional group (EC, KO)
      Args:
        reaction_tab (DataFrame): reaction/sample
        f2gtab (DataFrame): reaction/group
    """
    g2ftab = f2gtab.transpose()
    reaction_tab_a, g2ftab_a = _align_dataframe(reaction_tab, g2ftab)
    return g2ftab_a.dot(reaction_tab_a)
