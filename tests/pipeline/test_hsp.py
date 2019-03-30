import unittest

import os
import pandas as pd

from cmnet.pipeline.hsp import castor_hsp_workflow, castor_hsp, castor_nsti
from cmnet.utils import get_project_dir

# Read in expected output files.
test_dir_path = os.path.join(get_project_dir(), "tests", "test_data", "hsp")

in_traits1 = os.path.join(test_dir_path, "known_traits.tsv.gz")
in_tree1 = os.path.join(test_dir_path, "tree.tre")

hsp_mp_pred = os.path.join(test_dir_path, "hsp_output", "mp_pred_out.tsv")
hsp_mp_pred_nsti = os.path.join(test_dir_path, "hsp_output",
                             "mp_pred_out_nsti.tsv")
hsp_emp_prob_pred_ci = os.path.join(test_dir_path, "hsp_output", "emp_prob_pred_out_ci.tsv")

hsp_emp_prob_pred = os.path.join(test_dir_path, "hsp_output",
                              "emp_prob_pred_out.tsv")
hsp_pic_pred = os.path.join(test_dir_path, "hsp_output", "pic_pred_out.tsv")
hsp_scp_pred = os.path.join(test_dir_path, "hsp_output", "scp_pred_out.tsv")
hsp_subtree_average_pred = os.path.join(test_dir_path, "hsp_output",
                                     "subtree_average_pred_out.tsv")

# Read result
hsp_mp_pred_in = pd.read_table(hsp_mp_pred, sep="\t", index_col="sequence")

hsp_mp_pred_in_nsti = pd.read_table(hsp_mp_pred_nsti, sep="\t",
                                    index_col="sequence")

hsp_emp_prob_pred_in_ci = pd.read_table(hsp_emp_prob_pred_ci, sep="\t",
                                  index_col="sequence")

hsp_emp_prob_pred_in = pd.read_table(hsp_emp_prob_pred, sep="\t",
                                     index_col="sequence")
hsp_pic_pred_in = pd.read_table(hsp_pic_pred, sep="\t", index_col="sequence")
hsp_scp_pred_in = pd.read_table(hsp_scp_pred, sep="\t", index_col="sequence")
hsp_subtree_average_pred_in = pd.read_table(hsp_subtree_average_pred, sep="\t",
                                            index_col="sequence")

class Test_HSP_Dataset(unittest.TestCase):

    def test_default_table_checksum(self):
        # Check the attach files checksum.
        self.skipTest("Don't have time to do this yet.")


class Test_HSP_wrapper(unittest.TestCase):

    #  Test wrapper
    def test_mp_simple(self):
        predict_out, ci_out = castor_hsp(tree_path=in_tree1, trait_tab=in_traits1,
                                         hsp_method="mp", ran_seed=10)
        pd.testing.assert_frame_equal(predict_out, hsp_mp_pred_in, check_like=True)
        assert ci_out is None

    def test_castor_hsp_emp_prob(self):
        '''Test that Emp Prob confidence intervals calculated correctly.'''

        predict_out, ci_out = castor_hsp(tree_path=in_tree1, trait_tab=in_traits1,
                                         hsp_method="emp_prob", ran_seed=10, calc_ci=True)
        pd.testing.assert_frame_equal(ci_out, hsp_emp_prob_pred_in_ci, check_like=True)
        assert ci_out is not None


    def test_nsti(self):
        '''Test that calculated NSTI values match expected.'''

        nsti_out = castor_nsti(tree_path=in_tree1, known_tips = in_traits1)

        # Check only NSTI column.
        hsp_mp_pred_in_nsti_subset = hsp_mp_pred_in_nsti.loc[:, ["metadata_NSTI"]]
        pd.testing.assert_frame_equal(nsti_out, hsp_mp_pred_in_nsti_subset, check_like=True)


class Test_HSP_workflow(unittest.TestCase):

    def test_emp_prob_ci(self):
        '''Test that Emp Prob confidence intervals calculated correctly.'''
        predict_out, ci_out = castor_hsp_workflow(tree_path=in_tree1,
                                                  trait_table_path=in_traits1,
                                                  hsp_method="emp_prob",
                                                  ran_seed=10,
                                                  calc_ci=True)

        pd.testing.assert_frame_equal(ci_out, hsp_emp_prob_pred_in_ci, check_like=True)


