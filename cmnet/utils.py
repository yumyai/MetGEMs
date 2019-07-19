# Utility scripts
#

import sys
import os
from os.path import abspath, dirname, isdir, join, exists
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

def which(file):
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, file)):
            return os.path.join(path, file)

    return None

def make_output_dir(dirpath, strict=False):
    """Make an output directory if it doesn't exist
    Returns the path to the directory
    dirpath -- a string describing the path to the directory
    strict -- if True, raise an exception if dir already
    exists
    """
    dirpath = abspath(dirpath)

    # Check if directory already exists
    if isdir(dirpath):
        if strict:
            err_str = "Directory '%s' already exists" % dirpath
            raise IOError(err_str)

        return dirpath
    try:
        os.makedirs(dirpath)
    except IOError as e:
        err_str = "Could not create directory '%s'. Are permissions set " +\
                  "correctly? Got error: '%s'" %e
        raise IOError(err_str)

    return dirpath


def read_otutable(fh):
    """ Read OTU table file
    """
    df = pd.read_csv(fh, sep="\t", header=0, index_col=0)
    return df


def read_taxatable(fh):
    """ Read taxa table from QIIME. Currently only work on Greengene
    """
    alignment = ["kingdom", "phylum", "class", "order", "family", "genus", "species"]  
    predf = pd.read_csv(fh, sep="\t", header=0)
    taxondf = pd.DataFrame.from_records(predf.Taxon.apply(gg_parse)).reindex(columns=alignment)
    df = pd.concat([predf["Feature ID"], taxondf, predf["Confidence"]], axis=1)
    df = df.set_index("Feature ID")
    return df


def read_16s_table(file:Path):
    """ Read 16s data as series
    """
    normRNA = pd.read_csv(file, sep="\t", index_col=0, squeeze=True).fillna(1).clip(1)
    normRNA.name = "rna_n"
    return normRNA


def read_m2f(fh):
    """ Read model2function. Keep NA since some analysis need it.
    """
    df = pd.read_csv(fh, sep="\t", index_col=0, header=0)
    return df


def read_grouper(fh):
    """ Read file for converting from function into KO/EC
    """
    df = pd.read_csv(fh, sep="\t", header=0)
    df.columns = ["reaction", "group"]
    # create a pivot table for transformation
    df["value"] = 1
    pivotdf = df.pivot(index="reaction", columns="group", values="value").fillna(0)
    return pivotdf

class TaxaStringError(ValueError):
    pass

def gg_parse(s):
    """ Parse taxonomy string in GG format. Return 7 levels of taxonomy.
       Args:
          s: taxonomy string in gg format (k__Kingdom; p__Phylum)
    """
    
    # TODO: Make it all lowercase
    abbr_dct = {"k": "kingdom", "p": "phylum", "c": "class", "o": "order",
                "f": "family", "g": "genus", "s": "species"}
    taxa_dct = {"kingdom": "", "phylum": "", "class": "", "order": "",
                "family": "", "genus": "", "species": ""}  # Because groupby exclude None value.
    items = s.split("; ")
   
    # Sanity check
    if not s.startswith("k__"):
        # Unidentified OTU
        return taxa_dct
    
    if len(items) > 7:
        raise TaxaStringError()
        
    for token in items:
        abbrv, taxa = token.split("__")
        taxa_lvl = abbr_dct[abbrv]
        taxa = taxa if taxa else ""  # If empty, leave it as empty string
        # If it is bracket, then remove it
        if len(taxa) > 0 and taxa[0] == "[" and taxa[-1] == "]":
            taxa = taxa[1:-1]
        
        taxa_dct[taxa_lvl] = taxa
        
    # Create species name since GG omit genus part
    if taxa_dct["genus"] != "" and taxa_dct["species"] != "":
        taxa_dct["species"] = taxa_dct["genus"] + "_" + taxa_dct["species"]
    
    return taxa_dct


def rdp_parse(s):
    """ Parse RDP taxonomy string with 7 level format (SILVA uses it.)
        D_0__Bacteria;D_1__Epsilonbacteraeota;D_2__Campylobacteria;D_3__Campylobacterales;D_4__Thiovulaceae;D_5__Sulfuricurvum;D_6__Sulfuricurvum sp. EW1
        The ambiguous_taxa will be convert to empty string.
    """
    abbr_dct = {"D_0": "kingdom", "D_1": "phylum", "D_2": "class", "D_3": "order",
                "D_4": "family", "D_5": "genus", "D_6": "species"}
    taxa_dct = {"kingdom": "", "phylum": "", "class": "", "order": "",
                "family": "", "genus": "", "species": ""}
    tokens = s.split(";")
    for token in tokens: # D_0__Bacteria, or Ambiguous_taxa
        if token == "Ambiguous_taxa":
            break
        taxLv, taxName = token.split("__")
        # Make the output behave like GG parse
        taxLv = abbr_dct[taxLv]
        taxa_dct[taxLv] = taxName
        
    return taxa_dct


def get_project_dir():
    """ Returns the top-level project directory (when used with pip install -e
    """
    current_file_path = abspath(__file__)
    current_dir_path = dirname(current_file_path)
    return dirname(current_dir_path)


def biom_to_pandas_df(biom_tab):
    '''Will convert from biom Table object to pandas dataframe.'''

    # Note this is based on James Morton's blog post:
    # http://mortonjt.blogspot.ca/2016/07/behind-scenes-with-biom-tables.html)
    return(pd.DataFrame(np.array(biom_tab.matrix_data.todense()),
                                 index=biom_tab.ids(axis='observation'),
                                 columns=biom_tab.ids(axis='sample')))


def read_seqabun(infile):
    '''Will read in sequence abundance table in either TSV, BIOM, or mothur
    shared format.'''

    # First check extension of input file. If extension is "biom" then read in
    # as BIOM table and return. This is expected to be the most common input.
    in_name, in_ext = os.splitext(infile)
    if in_ext == "biom":
        return(biom_to_pandas_df(biom.load_table(infile)))

    # Next check if input file is a mothur shared file or not by read in first
    # row only.
    mothur_format = False
    try:
        in_test = pd.read_table(filepath_or_buffer=infile, sep="\t", nrows=1)
        in_test_col = list(in_test.columns.values)
        if len(in_test_col) >= 4 and (in_test_col[0] == "label" and \
                                      in_test_col[1] == "Group" and \
                                      in_test_col[2] == "numOtus"):
            mothur_format = True
    except Exception:
        pass

    # If identified to be mothur format then remove extra columns, set "Group"
    # to be index (i.e. row) names and then transpose.
    if mothur_format:
        input_seqabun = pd.read_table(filepath_or_buffer=infile, sep="\t")
        input_seqabun.drop(labels=["label", "numOtus"], axis=1, inplace=True)
        input_seqabun.set_index(keys="Group", drop=True, inplace=True,
                                verify_integrity=True)
        input_seqabun.index.name = None
        return(input_seqabun.transpose())
    else:
        return(biom_to_pandas_df(biom.load_table(infile)))
