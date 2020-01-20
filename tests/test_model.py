

import gemmet.model as model
from gemmet.model import ASVData, Model

import os
import pandas as pd


gtestfile = "./tests/test_data/models/gmodel.tar.gz"
stestfile = "./tests/test_data/models/smodel.tar.gz"

class TestASVData:

    def test_aggregate(self):
        asvtab = pd.DataFrame.from_dict(
            {"otu1": [1,1,1],
             "otu2": [2,2,2],
             "otu3": [4,4,4],
             "otu4": [8,8,8],
             "otu5": [16,16,16]},
            orient="index")
        asvtab.columns = ["s1", "s2", "s3"]
        
        # The strip-downed taxonomy with only genus and species
        taxtab = pd.DataFrame.from_dict(
            {"otu1": ["Bacillus","Bacillus_atrophaeus"],
             "otu2": ["Bacillus", "Bacillus_atrophaeus"],
             "otu3": ["Bacillus", "Bacillus_cereus"],
             "otu4": ["Bacillus", "Bacillus_clausii"],
             "otu5": ["Anaerostipes", "Anaerostipes_hadrus"]},
            orient="index")
        taxtab.columns = ["genus", "species"]
        asvdat = ASVData(asvtab, taxtab)
        # Genus aggregate should have two model
        genus_agg = asvdat.aggregate("genus")
        assert genus_agg.shape == (2, 3)
        sp_agg = asvdat.aggregate("species")
        assert sp_agg.shape == (4,3)
        
    
class TestModel:

    def test_read_genus(self):
        m = model.Model.read_model(gtestfile)


    def test_read_species(self):
        m = model.Model.read_model(stestfile)
        
            
    def test_map2model(self):
        # Create mock model
        gmodel = pd.DataFrame.from_dict(
            {"Bacillus": [1,2,3,4],
             "Blautia": [1,2,3,4]},
             orient="index",
        )

        gmodel.columns = ["a", "b", "c", "d"]

        smodel = pd.DataFrame.from_dict(
            {"Bacillus_atrophaeus": [1,2,3,4],
             "Bacillus_cerius": [1,2,3,4],
             "Blautia_hansenii": [1,2,3,4]},
             orient="index",
             columns=["a", "b", "c", "d"]
        )

        otutab = pd.DataFrame.from_dict(
            {
                "otu1": [1,2,3],
                "otu2": [1,2,3],
                "otu3": [1,2,3]
            },
            orient="index",
            columns=["s1", "s2", "s3"]
        )

        # Genus only model

        # Species only model

        # Both model


# Bacteria Firmicutes Bacilli Bacillales Bacillaceae Bacillus Bacillus_atrophaeus        Bacillus_atrophaeus_ATCC_49822_1                        
# Bacteria Firmicutes Bacilli Bacillales Bacillaceae Bacillus Bacillus_cereus            Bacillus_cereus_AH187_F4810_72                          
# Bacteria Firmicutes Bacilli Bacillales Bacillaceae Bacillus Bacillus_cereus            Bacillus_cereus_G9842                                   
# Bacteria Firmicutes Bacilli Bacillales Bacillaceae Bacillus Bacillus_clausii           Bacillus_clausii_KSM_K16   

# Bacteria Firmicutes Clostridia Clostridiales Lachnospiraceae Anaerostipes Anaerostipes_hadrus       Anaerostipes_hadrus_DSM_3319        
# Bacteria Firmicutes Clostridia Clostridiales Lachnospiraceae Anaerostipes Anaerostipes_sp           Anaerostipes_sp_3_2_56FAA           
# Bacteria Firmicutes Clostridia Clostridiales Lachnospiraceae Blautia      Blautia_hansenii          Blautia_hansenii_VPI_C7_24_DSM_20583