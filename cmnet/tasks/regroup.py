""" Regroup reaction into KO or EC
"""

import argparse
from pandas import DataFrame
import numpy as np
import cmnet.default
from cmnet.default import default_map
from cmnet.utils import align_dataframe
import pandas as pd

def run():
    parser = argparse.ArgumentParser(
            description="Regroup AGORA's reaction into EC/KO",
            usage="cmnet regroup -i input.tsv -g ec/ko -o output.tsv")

    parser.add_argument("-i", "--input", type=argparse.FileType("r"),
                        required=True, help='Reaction table from markp')
    parser.add_argument("-g", "--group", type=str,
                        required=True, help='{ec, ko}')
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), required=True,
                        help='File name for output table')
    args = parser.parse_args()
    
    # Load input
    functiontab = pd.read_csv(args.input, sep="\t", header=0, index_col=0)

    # Load table
    if args.group not in ["ec", "ko"]:
        raise ValueError("This function grouper is not available")

    f2g = read_grouper(default_map[args.group.upper()])
    samplegroup = function2group(functiontab, f2g)
    # round number
    samplegroup = samplegroup.round(5)
    samplegroup.to_csv(args.output, sep="\t")

def read_grouper(fh):
    """ Read file contains information of reaction -> functional group
    """
    df = pd.read_csv(fh, sep="\t", header=0)
    df.columns = ["reaction", "group"]
    # use pivot table to ensure that  one reaction -> many functional would be transform correctly 
    df["value"] = 1
    pivotdf = df.pivot(index="reaction", columns="group", values="value").fillna(0)
    return pivotdf

def function2group(reaction_tab, f2gtab) -> DataFrame:
    """ Group reactions into other functional group (EC, KO)
      Args:
        reaction_tab (DataFrame): reaction/sample
        f2gtab (DataFrame): reaction/group
    """
    g2ftab = f2gtab.transpose()
    reaction_tab_a, g2ftab_a = align_dataframe(reaction_tab, g2ftab)
    return g2ftab_a.dot(reaction_tab_a)

def function2group_strat(reaction_tab, f2gtab) -> DataFrame:
    """ Group reaction into other functional group, but with stratified (means list all bacteria involve)
    """
    common_idx = reaction_tab.index.intersection(f2gtab.index)
    # Reshape both values to be compatible with each other
    expanda = reaction_tab.values.repeat(len(f2gtab.columns), axis=0)
    f2gtab_tf = f2gtab.reindex(common_idx).stack().to_frame()

    result = pd.DataFrame(expanda * (f2gtab_tf.values), index=f2gtab_tf.index, columns=reaction_tab.columns)

    return result