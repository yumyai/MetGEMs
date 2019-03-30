import unittest


class pathway_test(unittest.TestCase):

    testQuery = "./tests/test_data/protein_assignment/citrate_synthase_ecoli.fasta"

    def test_blast_assignment(self):
        self.fail()

if __name__ == "__main__":
    unittest.main()