""" Marker placement to the model
"""

import argparse
import cmnet.default
from cmnet.utils import read_otutable, read_taxatable
import pandas as pd
from pandas import DataFrame
import numpy as np

def run():
    parser = argparse.ArgumentParser(
            description="Calculate model's abundance from marker data",
            usage="cmnet markp -i input.fasta -t taxa.tsv")

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
    otutab = read_otutable(args.otutab)
    taxtab = read_taxatable(args.taxtsv)



def model_placement(otutab, otu_mapping) -> DataFrame:
    """ Mapping OTU into model. Currently just use linage name from otu_mapping

        Args:
          otutab (DataFrame): otu table (row as sample)
          otu_mapping (Series): Index as otu and value as group
    """
    grouping = otu_mapping.name
    otutab_with_model = (otutab.join(otu_mapping, how="left"))
    model_tab = (otutab_with_model
                       .groupby(grouping)
                       .aggregate(sum))
    return model_tab

def _calculate_level(otutab, taxtab, level):
    """ Currently support genus and species
    """

    if level not in ["species", "genus"]:
        raise ValueError("")
    taxtab[level]


def _calculate_stepwise(otutab, taxtab):
    _step = ["species", "genus", "family"]
    # Map as much as possible in species level


