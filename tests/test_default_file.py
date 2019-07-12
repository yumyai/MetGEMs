# Test an existence and correctness of default files and test files

import os
from cmnet.default import genus_tables, species_tables


class TestAttachFiles():

    def test_check_file(self):
        os.path.exists(genus_tables["model_reaction"])
        os.path.exists(genus_tables["16s"])
        os.path.exists(species_tables["model_reaction"])
        os.path.exists(species_tables["16s"])
