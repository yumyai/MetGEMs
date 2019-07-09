# Test the correctness of all utilities
#

from cmnet import utils

class TestIOFormat():

    otutab_f = "tests/test_data/utils/minimum_otu.tsv"
    taxtab_f = "tests/test_data/utils/minimum_tax.tsv"
    otutab = utils.read_otutable(otutab_f)
    taxtab = utils.read_taxatable(taxtab_f)

    def test_read_otu(self):
        assert TestIOFormat.otutab.index.name == " "
        assert TestIOFormat.otutab.shape == (3, 3)

    def test_read_tax(self):
        assert TestIOFormat.taxtab.index.name == "Feature ID"
        #assert TestIOFormat.taxtab.columns 

