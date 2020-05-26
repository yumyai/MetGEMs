# MetGEMs
## Installation
We recommend to install with pip in the conda environment.
```
conda create -n metgem_env python=3.7
conda activate songbird_env
git clone https://github.com/yumyai/MetGEM
cd MetGEM
pip install  .
```

## Running
Here we will run the example files provide with repository
```
# Download model
wget https://github.com/yumyai/MetGEM/blob/master/metgem/default_files/models/kmodels/core.tar.gz?raw=true -O ko_model.tar.gz
wget https://github.com/yumyai/MetGEM/blob/master/metgem/default_files/models/emodels/core.tar.gz?raw=true -O ec_model.tar.gz
# Download example files
wget https://raw.githubusercontent.com/yumyai/MetGEM/master/examples/feature-table.tsv -O otutab.tsv
wget https://raw.githubusercontent.com/yumyai/MetGEM/master/examples/taxonomy_gg.tsv -O taxtab.tsv

# Convert ASVs table into KO profiles
metgem markp -i otutab.tsv -t taxtab.tsv -m ko_model.tar.gz -o output_ko.tsv
# Convert ASVs table into EC profiles
metgem markp -i otutab.tsv -t taxtab.tsv -m ec_model.tar.gz -o output_ec.tsv
```
