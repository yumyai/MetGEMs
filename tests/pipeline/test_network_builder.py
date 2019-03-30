from unittest import TestCase

import os
from cmnet.pipeline.network_builder import read_cyc_dat, record_to_reaction, network_builder_workflow
from cmnet.utils import get_project_dir

from cmnet.model.pathway import Reaction, MetabolicNetwork


test_dir = os.path.join(get_project_dir(), "tests")
test_reaction = os.path.join(test_dir, "test_data", "build_network", "metacyc_reactions.dat")
test_pathway = os.path.join(test_dir, "test_data", "build_network", "pathway_sample.dat")
# For test building TCA
test_tca_reactions_dat = os.path.join(test_dir, "test_data", "build_network", "test_reaction_TCA.dat")
test_tca_reactions_tsv = os.path.join(test_dir, "test_data", "build_network", "test_trait_TCA.tsv")

# Simple dataset
dct_simple = {"UNIQUE-ID": "id-1",
              "": "",
              "": ""}   # Have all needed key

dct_missing = {"UNIQUE-ID": "something"}

class TestCycParse(TestCase):
    """ Test if cyc data is read correctly

    """

    def test_read_dat(self):
        # An very simple test, read all dat files without error,
        # TODO: add expectation
        read_cyc_dat(test_reaction)

    def test_convert_reaction(self):
        # Convert dictionary from parsing dats into Reaction object.
        record_to_reaction(dct_simple)
        self.fail()


class TestNetworkBuilder(TestCase):

    def test_add_reactions(self):
        r1 = Reaction(id="01", types=["a", "b"], name="first", left=[], right=[],
                      subreaction=[], ecnum="1.1.1.1", taxonomy="ling")
        r2 = Reaction(id="02", types=["a"], name="second", left=[], right=[],
                      subreaction=[], ecnum="2.2.2.2", taxonomy="ling")
        mn = MetabolicNetwork("TestNetwork")
        mn.add_reaction(r1)
        mn.add_reaction(r2)
        # Check.


    def test_build_tca_cycle(self):
        # TCA cycle is a good example to try because it contains these.
        # 1. Complex reaction 2. Simple reaction 3. Cyclic. 4. Spontaneous reaction
        pass

    def test_network_workflow(self):
        # Test network workflow by building TCA cycle
        network_builder_workflow()

    def test_network_edge_case(self):
        # One with multiple enzyme like  KDPGALDOL-RXN

        # One with no enzyme
        pass


