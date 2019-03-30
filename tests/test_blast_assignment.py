from unittest import TestCase


class protein_assignment_test(TestCase):

    testQuery = "./tests/test_data/protein_assignment/citrate_synthase_ecoli.fasta"

    def test_blast_assignment(self):
        self.skipTest("Not sure if should be implement here.")
