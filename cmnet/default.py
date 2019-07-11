# List of default files for mapping
import os
from os import path
from cmnet.utils import get_project_dir

# Default support files packaged with CMNET
#   For genus assignment
_project_dir = get_project_dir()

#   For state prediction
genus_dir = path.join(_project_dir, "default_files", "genus_level")

genus_tables = {"model_reaction": path.join(genus_dir, "agora.reaction.gmean.tsv"),
                "KO":       path.join(genus_dir, "ko.tsv.gz")}

species_dir = path.join(_project_dir, "default_files", "species_level")

species_tables = {"model_reaction": path.join(genus_dir, "agora.reaction.smean.tsv"),
                  "KO":       path.join(species_dir, "ko.tsv.gz")}


# Initialize reaction mapfiles for converting AGORA reaction into other type
map_dir = path.join(_project_dir, "default_files", "map_files")

default_map = {"KO": "reaction_ko.tsv",
               "EC": "reaction_ec.tsv"}

#default_tables = {"16S": path.join(prokaryotic_dir, "16S.txt.gz"),
#
#                  "COG": path.join(prokaryotic_dir, "cog.txt.gz"),
#
#                  "EC": path.join(prokaryotic_dir, "ec.txt.gz"),
#
#                  "KO": path.join(prokaryotic_dir, "ko.txt.gz"),
#
#                  "PFAM": path.join(prokaryotic_dir, "pfam.txt.gz"),
#
#                  "TIGRFAM": path.join(prokaryotic_dir, "tigrfam.txt.gz")}
