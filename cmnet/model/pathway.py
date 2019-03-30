# Module for high-level manipulation such as parsing and visualize of network data.
#

from enum import Enum
from typing import NamedTuple, List
from collections import defaultdict
import networkx as nx

class MetabolicNetwork(object):
    """Class representation of metabolic network.
       Nodes represent metabolite and enzyme.
    """

    def __init__(self, name):
        self._name = name
        self._network = nx.DiGraph()
        self._reaction = {}  # ReactionID -> Object
        self._matrix = []  # Matrix that could be used in COBRA
        self._gene = {}  # GeneID -> [List]
        self._metabolite = {}  # Common-name -> ID
        # Chemical that use very frequent in pathway/network such as WATER
        self._common_metabolite = set(["WATER", "PROTON", "ADP", "NADP", "NADPH"])


    def add_reaction(self, reaction):
        """ Add reaction into network.

        Args:
            reaction:

        Returns:

        """
        # Extract id from reaction object
        nodes = reaction.left + reaction.right
        edge = reaction.ecnum  # Edge should be unique

        # Make an ID for enzyme and metabolites object,
        # Because the how metabolite/gene represent in reaction.dat seems to be not reliable.
        # Sometime they just use TYPE instead of name?
        # Assume that all metabolite's name is standardize.

        # It is possible that one reaction can have multiple enzyme
        edge = tuple(edge)
        ",".join(sorted(edge))
        # Check for metabolite that is common (WATER, Pi), and fan it out (WATER-001, WATER-002)


        # Put reaction ID into attribute so we can remember where it came from.
        # TODO: Put pathway ID into it to see overlap later

        self._network.add_node()

    def add_protein(self):
        pass

    def add_metabolite(self):
        pass

    def is_reaction_existed(self, reaction):
        """ Check if the reaction is already existed.

        Args:
            reaction: Reaction's object

        Returns:
            bool: True if it existed

        """
        nodes = reaction.left + reaction.right
        edge = reaction.ecnum  # Edge should be unique

        # Check if reaction with an exact same start/end and edge exists.
        for metabolite in nodes:
            pass
        pass


    def _paranoid_check(self):
        # Just a check if something went wrong, maybe a typo in your metabolite?
        # Check if any node (metabolite) has more than 50 edges connect to it.
        # Make in dangling instead.

        pass

    def _check_common_metabolite(self):
        """ Prune 'metabolite' that appears in many of reaction such as water, ATP, ADP,
        """
        pass

class Pathway(object):
    """ A subset of metabolic network.
    """

    def __init__(self, id_, name, network):
        self._id = id_
        self._name = name
        self._reactions = {}
        self._links = {}  # Since pathway is pretty small, adjacent list should be enough.

    def add_reaction(self, reaction):
        if reaction.name in self._reactions:
            raise ValueError("Duplicate ID in reaction entries")

        self._reactions[reaction.name] = reaction

    def add_link(self, id1, id2):
        """Add link between two reaction"""
        pass

    def __iter__(self):
        for reaction in self._reactions:
            yield reaction


class Chem(NamedTuple):
    id: str
    name: str


class Protein(NamedTuple):
    id: str
    name: str
    ecnum: str
    id_link: dict


class Gene(NamedTuple):
    id: str
    prot: Protein


class Taxa(NamedTuple):
    id: str
    name: str


class Reaction(NamedTuple):
    id: str
    types: List[str]  # Reaction type, sponta? #
    name: str
    left: List[str]
    right: List[str]
    subreaction: List[str]
    ecnum: str
    taxonomy: str


class Mapper(object):
    """ For finding
    """

    def __init__(self):
        pass


