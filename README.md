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
wget https://github.com/yumyai/MetGEM/blob/master/metgem/default_files/models/kmodels/core.tar.gz?raw=true -O model.tar.gz
# Download example files
wget https://raw.githubusercontent.com/yumyai/MetGEM/master/examples/feature-table.tsv -O otutab.tsv
wget https://raw.githubusercontent.com/yumyai/MetGEM/master/examples/taxonomy_gg.tsv -O taxtab.tsv

metgem markp -i otutab.tsv -t taxtab.tsv -m model.tar.gz -o output.tsv
```
