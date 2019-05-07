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
        self._pathway = set()
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
        edge = reaction.ecnum  # Edge should be unique.

        # Make an ID for enzyme and metabolites object,
        # Because the how metabolite/gene represent in reaction.dat seems to be not reliable.
        # Sometime they just use TYPE instead of name?
        # Assume that all metabolite's name is standardize.

        # It is possible that one reaction can have multiple enzyme, but I hope not
        edge = tuple(edge)
        ",".join(sorted(edge))
        # TODO: Check for metabolite that is common (WATER, Pi), and put it out (WATER-001, WATER-002)

        # Put reaction ID into attribute so we can remember where it came from.
        # TODO: Put pathway ID into it to see overlap later

        # It seems like node with the same ID won't get duplicate, no need to check it.
        self._network.add_nodes_from(nodes)
        self._network.add_edge(key=reaction.id)

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

    def add_pathway(self, pathway):

        if pathway.id in self._pathway:
            pass
        # Check if there is a link with previous pathway.




    def _paranoid_check(self):
        # Just a check if something went wrong, maybe a typo in your metabolite?
        # Check if any node (metabolite) has more than 50 edges connect to it.
        # Make in dangling instead.

        pass

    def _check_common_metabolite(self):
        """ Prune 'metabolite' that appears in many of reaction such as water, ATP, ADP,
        """
        pass


class Pathway(NamedTuple):
    id: str
    inpathway: str
    superpathway: str

class Reaction(NamedTuple):
    id: str
    types: List[str]  # Reaction type, sponta? #
    name: str
    left: List[str]
    right: List[str]
    subreaction: List[str]
    ecnum: str
    taxonomy: str

class ReactionPrimary(NamedTuple):
    # Only look at primary metabolite and simplified a bunch of thing.
    id: str
    left: str
    right: str
    ecnum: str

class Mapper(object):
    """ For finding
    """

    def __init__(self):
        pass


