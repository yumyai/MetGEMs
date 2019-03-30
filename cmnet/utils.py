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


def read_stockholm(filename, clean_char=True):
    '''Reads in Stockholm formatted multiple sequence alignment and returns
    dictionary with ids as keys and full concatenated sequences as values. When
    clean_char=True this function will convert all characters to uppercase and
    convert "." characters to "-". This was originally written for converting
    hmmalign output files.'''

    # Intitialize defaultdict that will contain strings.
    seqs = defaultdict(str)

    line_count = 0

    # Read in file line-by-line.
    with open(filename, "r") as stockholm:

        for line in stockholm:

            line = line.rstrip()

            # Header-line - check that it starts with "# STOCKHOLM".
            if line_count == 0 and "# STOCKHOLM" not in line:
                sys.exit("Error - stockholm format multiple-sequence "
                         "alignments should have \"# STOCKHOLM\" (and the "
                         "version number) on the first line")

            line_count += 1

            # Skip blank lines, lines that start with comment, and lines that
            # start with "//".
            if not line or line[0] == "#" or line[0:2] == "//":
                continue

            line_split = line.split()

            if clean_char:
                line_split[1] = line_split[1].upper()
                line_split[1] = line_split[1].replace(".", "-")

            # Add sequence to dictionary.
            seqs[line_split[0]] += line_split[1]

    # Double-check that last line was "//"
    if line[0:2] != "//":
        raise ValueError('Error - last line of stockholm file should have been \"//\".')
    return seqs

def read_fasta(infile, cut_header=False):

    '''Read in FASTA file and return dictionary with each independent sequence
    id as a key and the corresponding sequence string as the value.
    '''

    seq = {}
    name = None

    # Read in FASTA line-by-line.
    with open(infile, "r") as fasta:

        for line in fasta:
            line = line.strip()

            # If header-line then split by whitespace, take the first element,
            # and define the sequence name as everything after the ">".
            if line[0] == ">":

                line = line[1:]  # remove >

                if cut_header:
                    name = line.split()[0]
                else:
                    name = line

                # Intitialize empty sequence with this id.
                seq[name] = ""

            else:
                # Add sequence to dictionary.
                seq[name] += line

    return seq

def write_fasta(seqs, outfile):

    with open(outfile, "w") as fh:
        for seqname in seqs:
            fh.write(">" + seqname + os.linesep)
            fh.write(seqs[seqname] + os.linesep)


def biom_to_pandas_df(biom_tab):
    '''Will convert from biom Table object to pandas dataframe.'''

    # Note this is based on James Morton's blog post:
    # http://mortonjt.blogspot.ca/2016/07/behind-scenes-with-biom-tables.html)

    return(pd.DataFrame(np.array(biom_tab.matrix_data.todense()),
                                 index=biom_tab.ids(axis='observation'),
                                 columns=biom_tab.ids(axis='sample')))

def get_project_dir():
    """ Returns the top-level project directory (when used with pip install -e
    """
    current_file_path = abspath(__file__)
    current_dir_path = dirname(current_file_path)
    return dirname(current_dir_path)

def read_trait_table(file:Path):
    """ Read trait table


    Read a trait table and return pandas.

    Args:
        file:

    Returns:

    """
    return pd.read_csv(file, index_col="assembly", dtype={'sequence' : str})
