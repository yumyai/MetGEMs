from unittest import TestCase
from os import path
from tempfile import TemporaryDirectory

import pandas as pd

test_dir_path = path.join(path.dirname(path.abspath(__file__)), "test_data",
                          "metagenome_pipeline")

seqtab_biom = path.join(test_dir_path, "test_input_sequence_abun.biom")
seqtab_tsv = path.join(test_dir_path, "test_input_sequence_abun.tsv")
seqtab_msf = path.join(test_dir_path, "test_input_sequence_abun.msf")

func_predict = path.join(test_dir_path, "test_predicted_func.tsv")
marker_predict = path.join(test_dir_path, "test_predicted_marker.tsv")

nsti_in_path = path.join(test_dir_path, "test_nsti_in.tsv")

exp_strat = path.join(test_dir_path, "metagenome_out",
                      "pred_metagenome_strat.tsv")

exp_unstrat = path.join(test_dir_path, "metagenome_out",
                        "pred_metagenome_unstrat.tsv")

exp_strat_rare = path.join(test_dir_path, "metagenome_out",
                           "pred_metagenome_strat_RARE.tsv")

exp_norm = path.join(test_dir_path, "metagenome_out", "seqtab_norm.tsv")

# Read in test inputs and expected files.
func_predict_in = pd.read_table(func_predict, sep="\t", index_col="sequence")
marker_predict_in = pd.read_table(marker_predict, sep="\t",
                                  index_col="sequence")

exp_strat_in = pd.read_table(exp_strat, sep="\t")
exp_strat_in = exp_strat_in.set_index(["function", "sequence"])

exp_strat_in_rare = pd.read_table(exp_strat_rare, sep="\t")
exp_strat_in_rare = exp_strat_in_rare.set_index(["function", "sequence"])


exp_unstrat_in = pd.read_table(exp_unstrat, sep="\t", index_col="function")

exp_norm_in = pd.read_table(exp_norm, sep="\t", index_col="normalized")

nsti_in = pd.read_table(nsti_in_path, sep="\t", index_col="sequence")

class TestPipeline(TestCase):

    def test_pipeilne(self):
        pass

    def test_epa_to_hsp(self):
        self.fail()

    def test_hsp_to_metagenome(self):
        self.fail()

    def test_metagenome_to_network(self):
        self.fail()
