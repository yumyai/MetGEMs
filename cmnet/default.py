# List of default files for mapping
import os
from os import path
from cmnet.utils import get_project_dir

# Default support files packaged with CMNET
#   For genus assignment
#_project_dir = get_project_dir()
_project_dir = path.dirname(path.abspath(__file__))

#   For state prediction
genus_dir = path.join(_project_dir, "default_files", "genus_level")

genus_tables = {"model_reaction": path.join(genus_dir, "agora.reaction.gmean.tsv"),
        "16s":  path.join(genus_dir, "16s.tsv")}

species_dir = path.join(_project_dir, "default_files", "species_level")

species_tables = {"model_reaction": path.join(species_dir, "agora.reaction.smean.tsv"),
                  "16s":       path.join(species_dir, "16s.tsv")}

# Initialize reaction mapfiles for converting AGORA reaction into other type
map_dir = path.join(_project_dir, "default_files", "map_files")

default_map = {"KO": path.join(map_dir, "reaction_ko.tsv"),
               "EC": path.join(map_dir, "reaction_ec.tsv")}
