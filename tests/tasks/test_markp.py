# Test model placement

import pandas as pd
from cmnet.tasks.markp import model_placement as mp

# create test data
MAIN = pd.DataFrame({"S1": [1,1,1], "S2": [2,2,0], "S3": [0,1,1], "S4": [0,0,0]}, index=["otu1", "otu2", "otu3"])
TAXA = pd.Series(["Bacil", "Bifi", "Bifi"], index=["otu1", "otu2", "otu3"])
TAXA.name="genus"

def test_model_placement():
    results = mp(MAIN, TAXA)
    assert sorted(list(results.columns)) == ["S1", "S2", "S3", "S4"]  # has all columns
    # Same linage is collapse together
    assert list(results["S4"]) == [0, 0]
    assert list(results["S1"]) == [1, 2]
