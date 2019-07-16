# Test the correctness of all utilities
#

import pytest
import pandas as pd
from cmnet import utils

class TestIOFormat():

    otutab_f = "tests/test_data/utils/minimum_otu.tsv"
    taxtab_f = "tests/test_data/utils/minimum_tax.tsv"
    rrnatab_f = "tests/test_data/utils/minimum_16s.tsv"


    def test_read_otu(self):
        otutab = utils.read_otutable(TestIOFormat.otutab_f)
        assert otutab.index.name == " "
        assert otutab.shape == (3, 3)

    def test_read_tax(self):
        taxtab = utils.read_taxatable(TestIOFormat.taxtab_f)
        assert taxtab.index.name == "Feature ID"

    def test_read_16s(self):
        rrnaSeries = utils.read_16s_table(TestIOFormat.rrnatab_f)
        assert isinstance(rrnaSeries, pd.Series)
        assert len(rrnaSeries) == 6  # Correct number
        assert sum(pd.isna(rrnaSeries)) == 0   # NA should be fill
        assert sum(rrnaSeries == 0) == 0   # 0 should be fill

    def test_read_m2f(self):
        pass
