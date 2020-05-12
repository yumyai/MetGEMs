""" Run the pipeline
"""

import argparse
import logging

import pandas as pd
from pandas import DataFrame
import numpy as np

from metgem.tasks.markp import *
from metgem.tasks.regroup import *

def run():
    parser = argparse.ArgumentParser(
            description="Calculate model's abundance from marker data",
            usage="metgem markp -i otu.tsv -t taxa.tsv -m [genus/species/hybrid] -o output.tsv")

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
    if "," in args.model:
        for model in args.model.split(","):
            default_model[model]
        
    model = Model.read_model(default_model[args.model])
    # Combine multiple model
    normmodeltab = model.map2model(asvdata)
    normmodeltab.to_csv(args.output, sep="\t")

    f2k = read_grouper(default_map["KO"])
    f2e = read_grouper(default_map["EC"])
    samplekogroup = function2group(normmodeltab, f2k).to_csv("out1.tsv", sep="\t")
    sampleecgroup = function2group(normmodeltab, f2e).to_csv("out2.tsv", sep="\t")
