# Test an existence and correctness of default files and test files

import os
from cmnet.default import genus_tables, species_tables


class TestAttachFiles():

    def test_check_file(self):
        os.path.exists(genus_tables["reaction"])
        os.path.exists(genus_tables["KO"])
        os.path.exists(species_tables["reaction"])
        os.path.exists(species_tables["KO"])
