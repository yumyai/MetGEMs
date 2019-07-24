""" Marker placement to the model
"""

import argparse
import cmnet.default
from cmnet.default import default_map
from cmnet.utils import read_otutable, read_taxatable, read_16s_table, read_m2f, read_grouper, _align_dataframe
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
    modelcon = None
    if level == "genus":
        modelcon = cmnet.default.genus_tables
    elif level == "species":
        modelcon = cmnet.default.species_tables

    # Initialize all
    rRNANorm = read_16s_table(modelcon["16s"])
    m2ftab = read_m2f(modelcon["model_reaction"]).fillna(0)
    modeltab = model_placement(otutab, taxtab[level])  # otu -> model
    normmodeltab = normalize_16s(modeltab, rRNANorm)  # model -> normmodel
    functiontab = model2function(normmodeltab, m2ftab)
    functiontab.to_csv(args.output, sep="\t")
    # Just convert to both ec and ko for now.
    #f2k = read_grouper(default_map["KO"])
    #f2e = read_grouper(default_map["EC"])
    #samplekogroup = function2group(functiontab, f2k).to_csv("out1.tsv", sep="\t")
    #sampleecgroup = function2group(functiontab, f2e).to_csv("out2.tsv", sep="\t")
    

def _relative_abundance(df):
    """ Convert into relative abundance
    """
    return 100 * df / df.sum(axis=0)

def model2function(modeltab, m2ftab):
    """ Extrapolate model to the function (reaction)
      Args:
        modeltab (DataFrame): model/sample dataframe.
        m2ftab (DataFrame): model/function dataframe.
    """
    f2btab = m2ftab.transpose()
    modeltab_a, f2btab_a = _align_dataframe(modeltab, f2btab)
    return f2btab_a.dot(modeltab_a)


def normalize_16s(modeltab, rrnaN):
    """ normalize number of organism with 16s
    Args:
      modeltab (DataFrame):
      rrnaN (Series):
    """
    divarr = rrnaN.reindex(modeltab.index, fill_value=1).values
    normmodeltab = modeltab.divide(divarr, axis=0)
    return normmodeltab


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
