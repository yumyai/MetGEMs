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
MetGEM is a software package for predicting functional composition of microbial communities using metabolic models.


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
1. ASV/OTU table that list the abundance of ASV/OTU of each sample. [example](https://github.com/yumyai/MetGEMs/blob/master/tests/test_data/otutab.tsv)
2. Taxonomy table. [example](https://github.com/yumyai/MetGEMs/blob/master/tests/test_data/taxtab.tsv)

MetGEM came with prebuilt functional models based on [AGORA's model](https://github.com/VirtualMetabolicHuman/AGORA).

#### Quick usage
#### 1) Download input data
We will use the example files for a quick demonstration how MetGEMs works.
```
wget https://raw.githubusercontent.com/yumyai/MetGEM/master/examples/feature-table.tsv -O otutab.tsv
wget https://raw.githubusercontent.com/yumyai/MetGEM/master/examples/taxonomy_gg.tsv -O taxtab.tsv
```
#### 2) Convert ASVs table into KO profiles and EC profiles
MetGEMs come bundle with all kind of models. `listmodel` command can be used to list all models include with the MetGEMs.
The commands to produce KO profile abundance and EC profile abundance are identicle except for the model part.
```
metgem markp -i otutab.tsv -t taxtab.tsv -m k_core -o output_ko.tsv
metgem markp -i otutab.tsv -t taxtab.tsv -m e_core -o output_ec.tsv
```

The result should be in `output_ko.tsv` and `output_ec.tsv` as KO abundance table and EC numbers abundance table respectively. There are others type of option available (pan, pan-weight), but we found that core and core-weight usually provide a good estimation in most situations.


#### Use cases
##### Convert taxonomy abundance table into KO IDs abundance table.
```
metgem markp -i otutab.tsv -t taxtab.tsv -m k_core -o output_ko.tsv
```

##### Convert taxonomy abundance table into EC numbers abundance table.
```
metgem markp -i otutab.tsv -t taxtab.tsv -m e_core -o output_ec.tsv
```

### <a name="gethelp"></a>Getting help
If you encounter bugs or having futher questions, you can create an issue at the [Issues page](https://github.com/yumyai/MetGEMs/issues). I will get in touch as soon as possible.
### <a name="cite"></a>Citing MetGEM
TODO.

### <a name="limit"></a>Limitations
- There is no way to independently assign a taxonomic weight outside include directly into a model.
- KO <-> EC conversion is not supported. While it is trivial, we notice that most EC <-> KO conversion are not 1-1 mapping so we would not recommend.
