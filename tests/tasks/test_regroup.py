import pytest
from metgem.tasks.regroup import function2group, function2group_strat
import pandas as pd

# Simple case, everything is aligned and no missing data
a = pd.DataFrame.from_dict({"reaction1":[1,2,3],
                            "reaction2":[0,1,0],
                            "reaction3":[1,1,5]}, orient="index", columns=["sample1", "sample2", "sample3"])

b = pd.DataFrame.from_dict({"reaction1":[1,1,1,1],
                            "reaction2":[2,1,0,1],
                            "reaction3":[2,4,2,2]}, orient="index", columns=["KO1", "KO2", "KO3", "KO4"])

def test_function2group():
    idx = b.columns
    col = a.columns
    expectDF = pd.DataFrame([[3,6,13],
                             [5,7,23],
                             [3,4,13],
                             [3,5,13]], index=idx, columns=col)

    assert expectDF.equals(function2group(a,b))
    
@pytest.mark.skip(reason="Not implement yet")
def test_function2group_strat():
    raise ValueError("Not test")