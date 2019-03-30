""" protein_assigment.py
Assign protein to the closest protein available in template.
The "matching system" are classified into two groups
1. Match by sequence 2. Match by attribute
"""

from collections import namedtuple
from subprocess import check_call

class Protein(object):
    """ Why do you existed?
    """

    def __init__(self, seq, metadata):
        self.metadata = {}

def _makeblastcommand(makeblastexec, input, name):
    from shutil import which
    pass

def _blastcommand(blastexec, query, output):
    pass

def blast_assignment(seq, blastdb):
    """ Assigns protein to template using 2-way BLAST.
    Args:
        seq: Protein sequence

    Returns:

    """
    # makeblastdb for both files.
    # Build list of argument
    pass

def multiple_alignment_assignment(seq, db):
    """ Assignment using HMMER

    Args:
        seq:
        db:

    Returns:

    """
    pass
