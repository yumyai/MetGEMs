""" Marker placement to the model
"""

import argparse
import logging

import pandas as pd
from pandas import DataFrame
import numpy as np

import cmnet.default
from cmnet.default import default_map, default_model
from cmnet.utils import read_otutable, read_taxatable, read_16s_table, read_m2f, align_dataframe
from cmnet.model import Model, ASVData

def run():
    parser = argparse.ArgumentParser(
            description="Calculate model's abundance from marker data",
            usage="cmnet markp -i otu.tsv -t taxa.tsv -m [genus/species/hybrid] -o output.tsv")

    parser.add_argument("-i", "--otutab", type=argparse.FileType("r"),
                        required=True, help='OTU table')
    parser.add_argument("-t", "--taxtsv", type=argparse.FileType("r"), required=True,
                        help='Linage files')
    parser.add_argument("-m", "--model", type=str, required=True, default="gmean",
                        help='Model to use')
    parser.add_argument("-o", "--output", type=argparse.FileType("w"), required=True,
                        help='Output table')
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
    """ Convert into relative abundance
    """
    return 100 * df / df.sum(axis=0)

# def model2function(modeltab, m2ftab):
#     """ Extrapolate model to the function (reaction)
#       Args:
#         modeltab (DataFrame): model/sample dataframe.
#         m2ftab (DataFrame): model/function dataframe.
#     """
#     f2btab = m2ftab.transpose()
#     modeltab_a, f2btab_a = align_dataframe(modeltab, f2btab)
#     return f2btab_a.dot(modeltab_a)


# def normalize_16s(modeltab, rrnaN):
#     """ normalize number of organism with 16s
#     Args:
#       modeltab (DataFrame):
#       rrnaN (Series):
#     """
#     divarr = rrnaN.reindex(modeltab.index, fill_value=1).values
#     normmodeltab = modeltab.divide(divarr, axis=0)
#     return normmodeltab


# def model_placement(otutab, otu_mapping) -> DataFrame:
#     """ Mapping OTU into model. Uses linage name from simple mapping.

#         Args:
#           otutab (DataFrame): otu table (row as sample)
#           otu_mapping (Series): Index as otu and value as mapping values
#     """
#     grouping = otu_mapping.name
#     otutab_with_model = (otutab.join(otu_mapping, how="left"))
#     model_tab = (otutab_with_model
#                        .groupby(grouping)
#                        .aggregate(sum))

#     model_tab.index.name = "model"
#     return model_tab


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


def function2group(reaction_tab, f2gtab) -> DataFrame:
    """ Group reactions into other functional group (EC, KO)
      Args:
        reaction_tab (DataFrame): reaction/sample
        f2gtab (DataFrame): reaction/group
    """
    g2ftab = f2gtab.transpose()
    reaction_tab_a, g2ftab_a = align_dataframe(reaction_tab, g2ftab)
    return g2ftab_a.dot(reaction_tab_a)