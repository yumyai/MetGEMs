# Pathway's IO module
#

from enum import Enum
from pathlib import Path
from collections import defaultdict
from typing import Generator

import pandas as pd

from cmnet.model.pathway import MetabolicNetwork, Pathway, Reaction
from cmnet.utils import read_trait_table


def network_builder_workflow(trait_tab, reaction_dat:Path):
    """ Workflow for building a reaction network


    Build metabolic network


    Args:
        trait_tab:


    Returns:

    """

    # Read trait_table
    trait_df = read_trait_table(trait_tab)

    for row in trait_df.iterrows():  # For each sample.
        pass


def build_reactions_repo(reaction_dat):
    """ Build reactions repository,
    Which mean it should has standard protein / metabolite id for reference.

    Args:
        reaction_dat: Reaction file to read

    Returns:

    """
    # Read reactions and separate them into a scaffold network.
    chemical = {}
    reactions = {}  # Normal enzymatic reaction
    spontaneous_reactions = {}
    complex_reactions = {}  # A combination of many reaction
    enzyme_list = {}  # Enzyme to reaction

    for record in read_cyc_dat(reaction_dat):
        reaction = record_to_reaction(record)
        # Check if it is a complex reaction
        if reaction.subreaction is not None:  # Skip composite reaction since they might give a shortcut (which we don't need)
            complex_reactions[reaction.id] = reaction
            continue
        elif reaction.taxonomy in "2" or not reaction.taxonomy:  # Use only one within bacterial kingdom
            if reaction.ecnum:
                reactions[reaction.id] = reaction
            else:
                spontaneous_reactions[reaction.id] = reaction

def build_network(reactions_list):
    for reaction in reactions_list:
        pass



def read_cyc_dat(path:Path) -> Generator[dict, None, None]:
    """ Read record into dictionary

    Args:
        path:

    Returns:

    """

    with open(path, "r") as fh:

        record = defaultdict(list)

        for line in fh:
            line = line.strip()
            if line.startswith("#"): # Skip comments
                continue
            elif line.startswith("//"):  # Start new reaction object
                yield(record)  # Easier to debug this way.
                record = defaultdict(list)
                continue
            elif line.startswith("/"):  # It is comment
                content = line[1:]
                record["COMMENT"].append(content)
            else:  # Collect all header as dictionary
                header, content = line.split(" - ", 1)  # I think there is some " - " inside data.
                record[header].append(content)


def record_to_reaction(record:dict):
    """ Convert record from dat's file into reactions object.

    Args:
        record:

    Returns:

    """
    # Mapping from header to attributes
    mapping = {
        "UNIQUE-ID": "id",
        "TYPES": "types",
        "COMMON-NAME": "name",
        "ATOM-MAPPINGS": None,
        "CANNOT-BALANCE?": None,
        "CITATIONS": None,
        "COMMENT": None,
        "CREDITS": None,
        "DATA-SOURCE": None,
        "DBLINKS": None,
        "DOCUMENTATION": None,
        "EC-NUMBER": "ecnum",
        "ENZYMATIC-REACTION": None,
        "ENZYMES-NOT-USED": None,
        "EQUILIBRIUM-CONSTANT": None,
        "HIDE-SLOT?": None,  # No record with this
        "IN-PATHWAY": None,
        "INSTANCE-NAME-TEMPLATE": None,
        "LEFT": "left",
        "MEMBER-SORT-FN": None,
        "ORPHAN?": None,
        "PATHOLOGIC-NAME-MATCHER-EVIDENCE": None,
        "PATHOLOGIC-PWY-EVIDENCE": None,
        "PHYSIOLOGICALLY-RELEVANT?": None,
        "PREDECESSORS": None,
        "PRIMARIES": None,
        "REACTION-DIRECTION": None,
        "REACTION-LIST": "subreaction",
        "REGULATED-BY": None,
        "REQUIREMENTS": None,  # No record with this either
        "RIGHT": "right",
        "RXN-LOCATIONS": None,
        "SIGNAL": None,
        "SPECIES": None,
        "SPONTANEOUS?": None,
        "STD-REDUCTION-POTENTIAL": None,
        "SYNONYMS": None,
        "SYSTEMATIC-NAME": None,
        "TAXONOMIC-RANGE": "taxonomy",  # If empty, it mean universal. ( I guess)
        "^COEFFICIENT": None,
        "^OFFICIAL?": None,
        "^COMPARTMENT": None}

    # We used list as a default, but most item should have one value.
    keep_as_list = ["LEFT", "RIGHT", "REACTION-LIST"]
    for k in record.keys():
        if k not in keep_as_list:
            record[k] = record[k][0]

    # Make sure that everything is either point left-to-right or reversible
    right_to_left = ["IRREVERSIBLE-RIGHT-TO-LEFT", "PHYSIOL-RIGHT-TO-LEFT", "RIGHT-TO-LEFT"]
    if record["REACTION-DIRECTION"] in right_to_left:
        temp = record["LEFT"]
        record["LEFT"] = record["RIGHT"]
        record["RIGHT"] = temp
        record["REACTION-DIRECTION"] = record["REACTION-DIRECTION"].replace("RIGHT-TO-LEFT", "LEFT-TO-RIGHT")

    # Convert all old-key into our pattern.
    for from_, to_ in mapping.items():
        if to_ is not None:
            if from_ in record:
                record[to_] = record[from_]  # change name
            else:
                record[to_] = []  # Create an empty value
        if from_ in record:  # Record doesn't contain every key. some record doesn't have COMMON-NAME
            del(record[from_])  # Clean key that we don't use, also sometimes,

    reaction = Reaction(**record)

    return reaction


def filter_reaction(reaction:Reaction):
    """ Filter reaction to make sure that they could be in the same network

    Args:
        reaction:

    Returns:

    """
    #1. By taxonomy,
    #There are several taxonomy range, one of it is
    #TAXONOMIC-RANGE - TAX-2 -> Eubacteria, Bacteria
    #TAXONOMIC-RANGE - TAX-2157 -> Mendosicutes, Archaebacteria
    #TAXONOMIC-RANGE - TAX-33090  -> Green plant
    #TAXONOMIC-RANGE - TAX-33208 -> metazoans, Animalia
    #TAXONOMIC-RANGE - TAX-4751 ->  Eukaryota, Opisthokonta
    if reaction.taxonomy != "2":  # Bacteria
        return False

    return True


def readSBML(smblfile: Path) -> MetabolicNetwork:
    """

    Args:
        smblfile: path to sbml file

    Returns:

    """

#
# Reaction parser
#

# def parse_cyc_enzreaction(s):
#     """ Because the reaction is full of stupid things like
#     1,2,4-trihydroxybenzene 1,2-dioxygenase hydroxyquinol + oxygen  <-->  2-maleylacetate + 2 H+
#     amphetamine <i>N</i>-monooxygenase  amphetamine + NADPH + oxygen  <-->  N-(1-phenylpropan-2-yl)hydroxylamine + NADP+ + H2O
#
#
#     Args:
#         s: String in enzyme.col
#
#     Returns:
#         left, right, reversible
#
#     """
#     left, right = s.split("<-->")
#     left = left.split(" + ") # Should be enough in most case
#     right = right.split(" + ") # Should be enough in most case
#     reversible = True
#
#     return [left, right, reversible]
