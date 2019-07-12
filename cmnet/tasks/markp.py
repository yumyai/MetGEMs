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
            usage="cmnet markp -i input.fasta -t taxa.tsv -m [genus/species] -o output.tsv")

    parser.add_argument("-i", "--otutab", type=argparse.FileType("r"),
                        required=True, help='OTU table')
    parser.add_argument("-t", "--taxtsv", type=argparse.FileType("r"), required=True,
                        help='Linage files')
    parser.add_argument("-m", "--model", type=str, required=True, default="genus",
                        help='Linage to used,')
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), required=True,
                        help='Output table')
    args = parser.parse_args()

    # Load table
    otutab = read_otutable(args.otutab)
    taxtab = read_taxatable(args.taxtsv)
    # Load default files according to the argument
    # Calculate number of model.
    level = args.model
    defaulttab = None
    if level == "genus":
        defaulttab = cmnet.default.genus_tables
    elif level == "species":
        defaulttab =  cmnet.default.species_tables
    
    modeltab = model_placement(otutab, taxtab[level])
    modeltab.to_csv(args.output, sep="\t")
    # Normalize 16s


def model2function(modeltab, function_tab):
    """ 
    """
    pass

def normalize_16s(modeltab, rrnaN):
    """
    Args:
      modeltab (DataFrame):
      rrnaN (Series):
    """
    divarr = rrnaN.reindex(modeltab.index, fill_value=1).values
    normmodeltab = modeltab.divide(divarr, axis=0)
    return normmodeltab



def _align_dataframe(main, converter):
    """ Align index / column for frictionless calculation
    The most use case is to align B/A for convert A/Sample into B/Sample.
    While pandas help in sorting index, it error when index does not exists.

    """
    # Make sure that they are at least compatible, at least 1 intersection
    MAINIDX = set(main.index).intersection(converter.column)
    assert len(MAINIDX) / len(main.index) > 0

    main = main.reindex(index=MAINIDX)
    converter = converter.reindex(columns=MAINIDX)

    return (main, converter)


def model_placement(otutab, otu_mapping) -> DataFrame:
    """ Mapping OTU into model. Uses linage name from simple mapping.

        Args:
          otutab (DataFrame): otu table (row as sample)
          otu_mapping (Series): Index as otu and value as mapping values
    """
    grouping = otu_mapping.name
    otutab_with_model = (otutab.join(otu_mapping, how="left"))
    model_tab = (otutab_with_model
                       .groupby(grouping)
                       .aggregate(sum))

    model_tab.index.name = "model"
    return model_tab

def model_function():
    pass

def _calculate_level(otutab, taxtab, level):
    """ Currently support genus and species
    """

    if level not in ["species", "genus"]:
        raise ValueError("")
    taxtab[level]


def _calculate_stepwise(otutab, taxtab):
    _step = ["species", "genus", "family"]
    # Map as much as possible in species level
    pass
