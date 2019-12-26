# Test model placement
# TODO: Most functions are move to model.py

import pandas as pd
# from cmnet.tasks.markp import model_placement as mp
# from cmnet.tasks.markp import normalize_16s as ns
# from cmnet.tasks.markp import model2function as mf


# create test data
# MAIN = pd.DataFrame({"S1": [1,1,1],
#                      "S2": [2,2,0],
#                      "S3": [0,1,1],
#                      "S4": [0,0,0]}, index=["otu1", "otu2", "otu3"])
# TAXA = pd.Series(["Bacil", "Bifi", "Bifi"], index=["otu1", "otu2", "otu3"])
# TAXA.name="genus"

# def test_model_placement():
#     # Model placement using linage information.
#     # Currently combine an OTU with same linage name
#     results = mp(MAIN, TAXA)
#     assert sorted(list(results.columns)) == ["S1", "S2", "S3", "S4"]  # has all columns
#     # Same linage is collapse together
#     assert list(results["S4"]) == [0, 0]
#     assert list(results["S1"]) == [1, 2]


# MODELTAB = pd.DataFrame({"S1":[4,8], "S2":[8,4], "S3":[8,0]}, index=["Bacil", "Bifi"])
# RRNA_N = pd.Series([1,2,4], index=["Cyano", "Bifi", "Bacil"])

# def test_model_normalization():
#     # Normalization model with rrnaCount
#     result = ns(MODELTAB, RRNA_N)
#     assert list(result["S1"]) == [1,4]
#     assert list(result["S2"]) == [2,2]
#     assert list(result["S3"]) == [2,0]

# #DF1 = pd.DataFrame({"S1":[1,2], "S2":[3,4]}, index=["M1", "M2"])
# #DF2 = pd.DataFrame({"M1":[], "M2":[]}, index=["r1","r2","r3"])
# def test_align_dataframe():
#     pass

# NORMMODELTAB = pd.DataFrame({"S1":[1,4], "S2":[2,2], "S3":[2,0]}, index=["Bacil", "Bifi"])
# def test_model2function():
#     # Since model is on the row size
#     pass
