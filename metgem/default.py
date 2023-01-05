# List of default files for mapping
import os
from os import path
import pathlib

# Default support files packaged with metgem
# For genus assignment
_project_dir = path.dirname(path.abspath(__file__))

# Initialize reaction mapfiles for converting AGORA reaction into other type
map_dir = path.join(_project_dir, "default_files", "map_files")

default_map = {
    "KO": path.join(map_dir, "reaction_ko.tsv"),
    "EC": path.join(map_dir, "reaction_ec.tsv"),
}

# Model list
model_dirs = path.join(_project_dir, "default_files", "models")
# Look into the default model
default_model = {}
for model in pathlib.Path(model_dirs).glob("**/*.tar.gz"):
    abspath = model.absolute()
    # Get basename, since it is .tar.gz so we need to split two times
    basename = os.path.splitext(abspath.stem)[0]
    default_model[basename] = abspath
