# MetGEMs

## Table of contents
- [Introduction](#intro)
- [Getting Started](#start)
  - [Installation](#install)
  - [General usage](#genuse)
  - [Getting help](#gethelp)
  - [Citing MetGEM](#cite)

- [Limitations](#limit)

## <a name="intro"></a>Introduction
MetGEM is a tool for predicting functional composition of microbial communities using metabolic models.


## <a name="start"></a>Getting Started
### <a name="install"></a>Installation
MetGEM has been tested with python 3.7 in linux environment only. We highly recommend to install MetGEM with pip in the conda environment. 

```
conda create -n metgem_env python=3.7
conda activate metgem_env
git clone https://github.com/yumyai/MetGEM
cd MetGEM
pip install  -e .
```
When finished, you should 

When all is done, running `metgem` should print out the list of available commands.

```
>metgem
METGEM - Community Metabolic Network predictor from

Usage: metgem <command> [options] <arguments>

Available command
markp - Calculate reaction
listmodel - List available model
```

### <a name="genuse"></a>General usage
MetGEM takes two tab-delimited tables as an input
1. ASV/OTU table that list the abundance of ASV/OTU of each sample. [example](https://github.com/yumyai/MetGEMs/blob/master/examples/feature-table.tsv)
2. Taxonomy table. [example](https://github.com/yumyai/MetGEMs/blob/master/examples/taxonomy_gg.tsv)
3. (Optional) Models files

MetGEM came with prebuilt functional models using [AGORA's model](https://github.com/VirtualMetabolicHuman/AGORA). Although using external model is possible, there is no official support yet.


#### Use cases
#### 1) Prepare input data
In this example, we will use the example files provide with repository.
```
wget https://raw.githubusercontent.com/yumyai/MetGEM/master/examples/feature-table.tsv -O otutab.tsv
wget https://raw.githubusercontent.com/yumyai/MetGEM/master/examples/taxonomy_gg.tsv -O taxtab.tsv
```
Addtionally, we download the model separately. In the real use, you could use the `listmodel` command to see the included models, but for the sake of simpliscity, we will download models instead

```
wget https://github.com/yumyai/MetGEM/blob/master/metgem/default_files/models/kmodels/core.tar.gz?raw=true -O ko_model.tar.gz
wget https://github.com/yumyai/MetGEM/blob/master/metgem/default_files/models/emodels/core.tar.gz?raw=true -O ec_model.tar.gz
```

#### 2) Convert ASVs table into KO profiles and EC profiles

The commands to produce KO profiles and EC profiles are identicle except for the model part. This is our deliberate design choice, since we found that converting between KO/EC is not straightforward precedure.
```
metgem markp -i otutab.tsv -t taxtab.tsv -m ko_model.tar.gz -o output_ko.tsv
metgem markp -i otutab.tsv -t taxtab.tsv -m ec_model.tar.gz -o output_ec.tsv
```

The result should be EC/KO tables.

### <a name="gethelp"></a>Getting help
If you encounter bugs or having futher questions, you can create an issue at the [Issues page](https://github.com/yumyai/MetGEMs/issues). I will get in touch as soon as possible.
### <a name="cite"></a>Citing MetGEM
Soon.


## Limitation
- There is no way to independently assign a taxonomic weight outside include directly into a model.
- KO <-> EC conversion is not supported.
