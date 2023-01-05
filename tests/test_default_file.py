# Test an existence and correctness of default files and test files

import os
from metgem.default import default_model

class TestAttachFiles():

    def test_check_file(self):
        os.path.exists(default_model["e_pan"])
        os.path.exists(default_model["e_pan_weight"])
