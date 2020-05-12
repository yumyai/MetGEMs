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
MetGEM need ASV count in tab-delimited format and taxonomic assignment in GreenGene annotation.
metgem markp -i <exampleotu> -t <exampletaxa> -m [genus/species/hybrid] -o output.tsv
