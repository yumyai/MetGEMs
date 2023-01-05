""" Marker placement to the model
"""

import argparse
import logging

import pandas as pd
from pandas import DataFrame
import numpy as np

import metgem.default
from metgem.default import default_map, default_model
from metgem.utils import (
    read_otutable,
    read_taxatable,
    read_16s_table,
    read_m2f,
    align_dataframe,
)
from metgem.model import Model, ASVData


def run():
    parser = argparse.ArgumentParser(
        description="Calculate model's abundance from marker data",
        usage="metgem markp -i otu.tsv -t taxa.tsv -m [genus/species/hybrid] -o output.tsv",
    )

    parser.add_argument(
        "-i", "--otutab", type=argparse.FileType("r"), required=True, help="OTU table"
    )
    parser.add_argument(
        "-t",
        "--taxtsv",
        type=argparse.FileType("r"),
        required=True,
        help="Linage files",
    )
    parser.add_argument(
        "-m", "--model", type=str, required=True, default="gmean", help="Model to use"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        required=True,
        help="Output table",
    )
    args = parser.parse_args()

    # Load table
    otutab = read_otutable(args.otutab)
    taxtab = read_taxatable(args.taxtsv)
    # create ASVData object and model.
    asvdata = ASVData(otutab, taxtab)
    # Calculate number of model.
    modelargs = args.model
    if ".tar.gz" in modelargs:  # Probally use external model
        models = [Model.read_model(m) for m in modelargs.split(",")]
    else:
        models = [Model.read_model(default_model[m]) for m in modelargs.split(",")]

    if len(models) == 1:
        model = models[0]
    else:
        # Combining multiple model have performance problem, only do it when one is empty
        model = models[0]
        for i in models[1:]:
            model += i
    modeltab = model.map2model(asvdata)
    modeltab.index.name = "reactions"
    modeltab.to_csv(args.output, sep="\t")


def _relative_abundance(df):
    """Convert into relative abundance"""
    return 100 * df / df.sum(axis=0)
