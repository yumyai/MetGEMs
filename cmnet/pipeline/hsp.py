""" Hidden State Prediction module
Using castor to predict hidden state (gene content, 16s copy number)

Calculateion
"""

import os
from math import ceil
from tempfile import TemporaryDirectory
from subprocess import check_call

import pandas as pd
from joblib import delayed, Parallel

from cmnet.utils import get_project_dir

def castor_hsp_workflow(tree_path: str,
                        trait_table_path: str,
                        hsp_method: str,
                        chunk_size:int = 500,
                        calc_nsti:bool = False,
                        calc_ci:bool = False,
                        check_input:bool = False,
                        num_proc:int = 1,
                        ran_seed: int = None):
    """ Run full HSP workflow.

    This run both HSP by split input into chunk and run on each.

    Args:
        tree_path:
        trait_table_path: Trait table file. See example from test file.
        hsp_method: either "mp", "emp_prob", "pic", "scp", "subtree_average"
        chunk_size:
        calc_nsti:
        calc_ci:
        check_input:
        num_proc:
        ran_seed:

    Returns:

    """

    # Read in trait table as pandas dataframe.

    if calc_nsti:
        nsti_values = castor_nsti(tree_path, trait_table_path)

    with TemporaryDirectory() as temp_dir:
        # Split trait table into multiple
        trait_tab = pd.read_table(trait_table_path, sep="\t", index_col="assembly", dtype = {'assembly': str})
        num_chunks = ceil(int(trait_tab.shape[1]) / (chunk_size + 1))

        trait_in_subset = []

        for i in range(num_chunks):
            subset_filename = os.path.join(temp_dir,  "subset_tab_" + str(i))
            (trait_tab.iloc[:, i * chunk_size:(i+1) * chunk_size].
               to_csv(subset_filename, index_label="assembly", sep="\t"))  # Split
            trait_in_subset.append(subset_filename)

        castor_out_raw = Parallel(n_jobs=num_proc)(delayed(castor_hsp)(tree_path,
                                                                       trait_in,
                                                                       hsp_method,
                                                                       calc_ci,
                                                                       check_input,
                                                                       ran_seed)
                                                   for trait_in in trait_in_subset)

        predicted_out_chunks, ci_out_chunks = zip(*castor_out_raw)
        assert len(castor_out_raw) == len(predicted_out_chunks)  # Sanity check
        #  Create base
        predicted_out_combined = pd.concat(predicted_out_chunks)
        ci_out_combined = None

        if calc_nsti:
            predicted_out_combined = pd.concat([predicted_out_combined, nsti_values], axis=1)

        if calc_ci:
            ci_out_combined = pd.concat(ci_out_chunks)

        return (predicted_out_combined, ci_out_combined)


def castor_hsp(tree_path:str,
               trait_tab:str,
               hsp_method:str,
               calc_ci:bool = False,
               check_input=False,
               ran_seed=None):
    """ Wrapper of castor's RScript


    Run a castor's RScript and return result to python.


    Args:
        tree_path:
        trait_tab: Table of trait for use as reference (row -> org, col -> trait)
        hsp_method: either "mp", "emp_prob", "pic", "scp", "subtree_average"
        calc_ci:

    Returns:

    """
    # Check R availability
    # Format boolean for R argument
    castor_hsp_script = os.path.join(get_project_dir(), 'cmnet', 'Rscripts', 'castor_hsp.R')
    if calc_ci:
        calc_ci_setting = "TRUE"
    else:
        calc_ci_setting = "FALSE"
    if check_input:
        check_input_setting = "TRUE"
    else:
        check_input_setting = "FALSE"

    with TemporaryDirectory() as temp_dir:

        # Temporary output for R
        output_count_path = os.path.join(temp_dir, "predicted_counts.txt")
        output_ci_path = os.path.join(temp_dir, "predicted_ci.txt")

        hsp_cmd = ["Rscript", castor_hsp_script, tree_path, trait_tab, hsp_method, calc_ci_setting,
                   check_input_setting, output_count_path, output_ci_path, str(ran_seed)]

        # Run castor_hsp.R
        check_call(hsp_cmd)

        # Load the output into Table objects
        try:
            asr_table = pd.read_table(filepath_or_buffer=output_count_path,
                                  sep="\t", index_col="sequence")
        except IOError:
            raise ValueError("Cannot read in expected output file" +
                            output_ci_path)

        if calc_ci:
            asr_ci_table = pd.read_table(filepath_or_buffer=output_ci_path,
                                  sep="\t", index_col="sequence")
        else:
            asr_ci_table = None

    # Return list with predicted counts and CIs.
    return [asr_table, asr_ci_table]

def castor_nsti(tree_path, known_tips):
    """ Calculate a score of each study sequence by looking for the closest reference on tree
    """

    castor_nsti_script = os.path.join(get_project_dir(), 'cmnet', 'Rscripts', 'castor_nsti.R')

    with TemporaryDirectory() as temp_dir:
        nsti_tmp_out =  os.path.join(temp_dir, "nsti_out.txt")
        check_call(["Rscript", castor_nsti_script, tree_path,
                    known_tips, nsti_tmp_out])

        # Read in calculated NSTI values.
        nsti_out = pd.read_table(nsti_tmp_out, sep="\t", index_col="sequence")

        # TODO: Move this into R script, it is not like we are going to intercept them anyway.
        # Make sure that the table has the correct number of rows.
        #if len(known_tips) != nsti_out.shape[0]:
        #    ValueError("Number of rows in returned NSTI table is incorrect.")

    return nsti_out
