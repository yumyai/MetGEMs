""" Model.py

    This module provides class for store and process.
"""

import logging
import warnings

import pandas as pd
import numpy as np
from pandas import DataFrame



class ASVData(object):
    """ Object for ASV table and taxonomy table.

    This object hold everything I need for metagenomics analysis (ok not EVERYTHING there is)
    """

    def __init__(self, asvtab:pd.DataFrame, taxtab:pd.DataFrame):
        self.asvtab = asvtab
        self.taxtab = taxtab
        self._self_check()

    def _self_check(self):
        """ Check format of asv and taxonomy table
        1. asvtab SHOULDN'T have taxonomyname
        2. index in both should be the same
        """
        # Check 
        np.intersect1d(self.asvtab.index, self.taxtab.index)
        return True

    def aggregate(self, level) -> DataFrame:
        """ Aggregate OTU/ASV with the same taxonomy 
        """
        group = self.taxtab[level]
        group.name = level
        modeltab = (self.asvtab.join(group, how="left")
          .groupby(level)
          .aggregate(sum))
        modeltab.index.name = "model"
        return modeltab

    def filter_by_asvid(self, otuid):
        """Filter by OTU list"""

        return ASVData(self.asvtab.reindex(otuid), self.taxtab.reindex(otuid))


class Model(object):
    
    def __init__(self, manifest, anumber, gmodel, smodel):
        self.manifest = manifest
        self.anumber = anumber
        self.gmodel = gmodel
        self.smodel = smodel
        
    def _validate_format(self):
        # Check format of input
        for i in [self.gmodel, self.smodel]:
            if not i.index.is_unique():
                return False
        
        return True
        
    def map2model(self, amplicondat: ASVData) -> DataFrame:
        """ Map amplicon data and turn it into model data
        """
        # Split the OTU table into species-match and genus-match, this to prevent mix-up.
        remaintaxa = amplicondat.taxtab.copy()
        # Match as much as species as it can, if not,  move it to upper level
        slvl_taxa = remaintaxa[remaintaxa.species.isin(self.smodel.index)].index
        remaintaxa = remaintaxa[~ remaintaxa.species.isin(self.smodel.index)]
        glvl_taxa = remaintaxa[remaintaxa.genus.isin(self.gmodel.index)].index
        # Convert OTU into model name
        amdat_slvl = amplicondat.filter_by_asvid(slvl_taxa).aggregate("species")
        amdat_glvl = amplicondat.filter_by_asvid(glvl_taxa).aggregate("genus")
        # Normalize with 16s
        if not self.anumber.empty:
            sdivide = self.anumber.reindex(amdat_slvl.index, fill_value=1).iloc[:,0].values
            gdivide = self.anumber.reindex(amdat_glvl.index, fill_value=1).iloc[:,0].values
            amdat_slvl = amdat_slvl.divide(sdivide, axis=0)
            amdat_glvl = amdat_glvl.divide(gdivide, axis=0)

        # Calculate model and combine, while this is not optimal, but it is easier to understand, inspect, and prevent mixed up
        # Replace OTU with model name
        smodeltab = self._convert_dataframe(amdat_slvl, self.smodel.transpose())
        gmodeltab = self._convert_dataframe(amdat_glvl, self.gmodel.transpose())
        modelsampletab = gmodeltab.add(smodeltab, fill_value=0)
        return modelsampletab

    def map2model_strat(self, amplicondat: ASVData) -> DataFrame:
        """ Map amplicon data and turn it into model data. Use stratified to keep
        """
        pass

    def _convert_dataframe(self, main: DataFrame, converter: DataFrame) -> DataFrame:
        """ Align dataframe and multiplication, converting for one-to-one
        
        Align dataframe multiply them

          Args:

        """
        mainidx = list(set(main.index).intersection(converter.columns))
        newmain = main.reindex(mainidx)
        newconverter = converter[mainidx]
        return newconverter.dot(newmain)


    @classmethod
    def read_model(cls, fh):
        """ Read model file and deserialize to 

        The model file is store in .tar.gz format. If the level of model does not exists, then it return empty data.frame (or None)
        """
        import tarfile

        def _try_read_files(filename, gzh):
            # Try read the file in hope i
            retdf = pd.DataFrame()
            try:
                innerhandle = gzh.extractfile(filename)
                retdf = pd.read_csv(innerhandle, sep="\t", index_col=0)
                retdf = retdf.fillna(0)
            except:
                pass

            return retdf
                
        gzh = tarfile.open(fh, mode="r:gz")
        # Check model's files
        fnames = [f.name for f in gzh.getmembers()]
        # Read manifest file
        mh = gzh.extractfile("manifest")
        mhtxt = mh.read()
        # Read model
        amplicon_df = _try_read_files("anumber.tsv", gzh)
        genus_df = _try_read_files("gmodel.tsv", gzh)
        species_df = _try_read_files("smodel.tsv", gzh)
        
        return cls(mhtxt, amplicon_df, genus_df, species_df)
    
    def __add__(self, aModel):
        # Since add takes really long time to combine if one is empty
        def _use_one(df1, df2):
            if df1.shape == (0,0):
                return df2
            if df2.shape == (0,0):
                return df1
            # If both zero, then it would be ok anyway.
            return df1.add(df2, fill_value=0)
        return Model("Merge between {} and {}".format(self.manifest, aModel.manifest),
                     _use_one(self.anumber, aModel.anumber),
                     _use_one(self.gmodel, aModel.gmodel),
                     _use_one(self.smodel, aModel.smodel))