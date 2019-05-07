# MetaCYC's IO module
# Since the data is s-expression, it looks like a nested-parenthesis

from pathlib import Path
from collections import defaultdict
import re  # For parsing most parenthesis
import itertools
from typing import Generator

import pandas as pd
import pyparsing

from cmnet.model.metabolicnetwork import MetabolicNetwork, Pathway, Reaction
from cmnet.utils import read_trait_table


from pyparsing import Forward, nestedExpr, Word, alphanums

# Test how to parse
enclosed = Forward()
nestedParens = nestedExpr('(', ')', content=enclosed)
enclosed << (Word(alphanums+'.'+'-'+':') | ',' | nestedParens)

def _parse_pathway_link(s):
    """ Parse PATHWAY-LINKS from metacyc

    :param s:
    :return:
    """
    parsed = enclosed.parseString(s).asList()
    direction = None  # not known
    connect = []
    primary_met = parsed[0]
    # A newer schema I guess
    if isinstance(parsed[1], list):  # (PATHWAY-LINKS - (CPD-7087 (PWY-5152 . :OUTGOING))
        direction = parsed[1][2]
        connect.append(parsed[1][0])
        connect.extend(parsed[2:])  # (NICOTINAMIDE_RIBOSE (TRANS-RXN0-481 . :INCOMING) NAD-BIOSYNTHESIS-II PWY-5381)
    else:
        connect.extend(parsed[1:])

    return (primary_met, direction, connect)

def _parse_reaction_layout(s):
    # Parsing reaction-layout
    # (RXN-10132 (:LEFT-PRIMARIES QUER) (:DIRECTION :L2R) (:RIGHT-PRIMARIES CPD-10894))
    # Into dictionary {"RXN-10132: [QUER,CPD-10894]"}
    # I want it cheap and fast
    # https://stackoverflow.com/questions/38999344/extract-string-within-parentheses-python
    parsed = enclosed.parseString(s).asList()  # TODO: Use this
    swap = False
    reaction_name = s[0]
    left = s[1].split(" ")[1]  # :LEFT-PRIMARIES
    if s[2].contains(":R2L"):  # :DIRECTION
        swap = True
    right = s[3].split(" ")[1]  # :RIGHT-PRIMARIES
    if swap:
        temp=right
        right=left
        left=temp

    return (reaction_name, left, right)

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

def _parse_super_pathway(record:dict):
    pass


def record_to_pathway(record:dict, reaction_ec):
    """Parse pathway since we need to link everything together

    :param record:
    :param reaction_ec: Dictionary of reaction -> ec-number
    :return:
    """

    mapping = {"UNIQUE-ID": "id",
            "TYPES": None,
            "COMMON-NAME": None,
            "CITATIONS": None,
            "CLASS-INSTANCE-LINKS": None,
            "COMMENT": None,
            "CREDITS": None,
            "DBLINKS": None,
            "ENZYME-USE": None,
            "HYPOTHETICAL-REACTIONS": None,
            "IN-PATHWAY": "inpathway",
            "NET-REACTION-EQUATION": None,
            "PATHWAY-INTERACTIONS": None,
            "PATHWAY-LINKS": "pathway_link",
            "POLYMERIZATION-LINKS": None,
            "PREDECESSORS": None,
            "PRIMARIES": None,
            "REACTION-LAYOUT": "reaction_layout",
            "REACTION-LIST": None,
            "SPECIES": None,
            "SUB-PATHWAYS": None,
            "SUPER-PATHWAYS": "superpathway",
            "SYNONYMS": None}

    # We used list as a default, but most item should have one value.
    #keep_as_list = ["IN-PATHWAY", "PRIMARIES", "REACTION-LIST", "REACTION-LAYOUT", "SPECIES"]
    #for k in record.keys():
    #    if k not in keep_as_list:
    #        record[k] = record[k][0]

    # SUPERPATHWAY doesn't have anything similar to it. sadly.
    if record["TYPES"] ==  "Super-Pathways":
        return _parse_super_pathway(record)

    reaction_layout = {}
    for line in record["REACTION-LAYOUT"]:
        reaction_name, left, right = _parse_reaction_layout(line)
        reaction_layout[reaction_name] = (left, right)
    record[reaction_layout] = reaction_layout

    # Predecessor tell how pathway hold itself, actually similar to reaction-layout
    pathway_layout = defaultdict(list)
    nodes = set()  # For later calculation
    for line in record["PREDECESSOR"]:
        s = line[1:-1]
        t, f = s.split(" ")  # Make sure to swap them
        nodes.add(f)
        nodes.add(t)
        pathway_layout[f].append(t)

    # We use an explicit link to other pathway. Just in case.
    # The end reaction is the one that does not point to any other reaction.
    endreactions = nodes - set(pathway_layout.keys())
    # The start reaction is the node that has no one pointing to
    startreactions = nodes - itertools.chain(*pathway_layout.values())  # All nodes - all target
    # Look at reaction_layout if it match something
    for line in record["PATHWAY-LINKS"]:
        prim_met, direction, connect_pth = _parse_pathway_link(line)

    # Convert all old-key into our pattern.
    for from_, to_ in mapping.items():
        if to_ is not None:
            if from_ in record:
                record[to_] = record[from_]  # change name
            else:
                record[to_] = []  # Create an empty value
        if from_ in record:  # Record doesn't contain every key. some record doesn't have COMMON-NAME
            del(record[from_])  # Clean key that we don't use, also sometimes,

    pathway = Pathway(**record)

    return pathway


def filter_reaction(reaction:Reaction):
    """ Filter reaction to the same species / locatoin

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
