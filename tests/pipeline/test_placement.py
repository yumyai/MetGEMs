from unittest import TestCase
import os
from tempfile import TemporaryDirectory

from cmnet.utils import get_project_dir
from cmnet.pipeline.placement import gappa_jplace_to_newick, run_epa_ng, seq_placement

# Set paths to test files.
test_dir_path = os.path.join(get_project_dir(), "tests")

test_study_seqs = os.path.join(test_dir_path, "test_data", "place_seqs",
                               "study_seqs_test.fasta")

test_tree = os.path.join(test_dir_path, "test_data", "place_seqs",
                         "img_centroid_16S_aligned_head30.tre")

test_msa = os.path.join(test_dir_path, "test_data", "place_seqs",
                        "img_centroid_16S_aligned_head30.fna")

test_hmm = os.path.join(test_dir_path, "test_data", "place_seqs",
                        "img_centroid_16S_aligned_head30.hmm")

exp_papara_phylip = os.path.join(test_dir_path, "test_data", "place_seqs",
                                 "place_seqs_output", "place_seqs_working",
                                 "papara_alignment.out")

exp_study_fasta = os.path.join(test_dir_path, "test_data", "place_seqs",
                               "place_seqs_output", "place_seqs_working",
                               "study_seqs_papara.fasta")

exp_ref_fasta = os.path.join(test_dir_path, "test_data", "place_seqs",
                             "place_seqs_output", "place_seqs_working",
                             "ref_seqs_papara.fasta")

exp_newick = os.path.join(test_dir_path, "test_data", "place_seqs",
                          "place_seqs_output",
                          "img_centroid_16S_aligned_head30_placed.tre")

exp_jplace = os.path.join(test_dir_path, "test_data", "place_seqs",
                          "place_seqs_output", "place_seqs_working",
                          "epa_out", "epa_result.jplace")


class TestPlacement(TestCase):

    def test_run_gappa(self):
        """Basic test run on gappa"""

        exp_newick_in = open(exp_newick).read()

        with TemporaryDirectory() as temp_dir:
            newick_out = os.path.join(temp_dir, "out.tre")

            gappa_jplace_to_newick(jplace_file=exp_jplace, outfile=newick_out)

            obs_newick_in = open(newick_out).read()

        self.assertEqual(exp_newick_in, obs_newick_in)

    def test_run_epa_ng(self):
        '''Basic test to check whether EPA-NG wrapper can be run. Exact
        matches to a treefile are not checked since slight differences
        are expected depending on different versions.'''

        with TemporaryDirectory() as temp_dir:
            run_epa_ng(ref_tree=test_tree,
                       ref_msa_fastafile=exp_ref_fasta,
                       study_msa_fastafile=exp_study_fasta,
                       out_dir=temp_dir)

    def test_seq_placement(self):
        """ Run workflow to see if there is a hiccup in it"""

        with TemporaryDirectory() as temp_dir:
            tmp_tree = os.path.join(temp_dir, "out.tre")
            seq_placement(test_study_seqs,
                          test_msa,
                          test_tree,
                          test_hmm,
                          out_tree=tmp_tree,
                          threads=1,
                          out_dir=temp_dir,
                          chunk_size=5000)
