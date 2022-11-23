# Chemical Space Generation

## Disclaimer

Portions of the code found in this repository and the general workflow used for the generation of chemical spaces have been adapted from an original publication by [Doyle and co-workers](https://doi.org/10.1021/jacs.1c12203).

## Abstract

The repository holds an implementation of a workflow reported by [Doyle and co-workers](https://doi.org/10.1021/jacs.1c12203) for the featurization and dimensionality reduction (UMAP) to generate data-science based chemical spaces. Based on this workflow, our group has generated a boronic acid chemical space, which has been used in works related to the cross-coupling of [bromotetrazines](https://doi.org/10.1021/acscatal.2c01813) and [bromotriazines](https://doi.org/10.1021/acs.joc.2c02082).

## Contents

This repository holds various folder, their contents are quickly described.

### Code

**Featurize.py:**

The code folder contains the Featurize.py script, which can be run on a science cloud or any machine to generate the raw featurization data used for the generation of chemical spaces. It is written in python and uses only standard modules (os and copy). However, it requires [OpenBabel](http://openbabel.org/wiki/Main_Page), ORCA, [XTB](https://xtb-docs.readthedocs.io/en/latest/setup.html), [CREST](https://xtb-docs.readthedocs.io/en/latest/crest.html), and [Multiwfn](http://sobereva.com/multiwfn/) to be installed. To download ORCA, you need to register on the [ORCA Forum](https://orcaforum.kofo.mpg.de/app.php/portal). An explanation of how ORCA works is beyond the scope of this summary. Still additional and useful information can be found in the [ORCA input library](https://sites.google.com/site/orcainputlibrary/home?pli=1). The output of the script is a folder structure that holds all the computed XTB, CREST, and ORCA files.

**Summarize_Featurization_Data.ipynb:**

This Jupyter Notebook reads in all featurization data from the folder structure generated by Featurize.py, truncates it to only contain the data relevant for chemical space generation, and outputs it as a .csv file. 

**Random_BA_Picking.ipynb:**

The notebook reads in data from a summarized .csv file, generates a chemical space, and picks one random substrate from every cluster.

**Dim_Reduction_and_UMAP_Plotting:**

Similar to the notbook above, .csv data is reada and a chemical space is generated. This notebook, however, can then be used to plot the resulting clusters in various ways.

### Featurization

The folder also contains the above described Featurize.py script along with all files necessary to perform a featurization. These are a dataset and two sets of input header and footer to generate ORCA input files. BA_dataset_1.txt contains SMILES of 730 boronic acids. BA_dataset_2.txt contains SMILES of ~2800 boronic acids. Br_dataset.txt contains SMILES of ~2600 aryl bromides and is identical to the dataset used by [Doyle and co-workers](https://doi.org/10.1021/jacs.1c12203). The input headers and footers contain additional information for the generation of ORCA input files and can be modified as needed. With the current Featurize.py setup the initial geometry optimization uses the "_geo_opt" suffixed files and the featurization uses the other set of files.

### Ready to Run

This folder contains two collections of files which can be run as is. The respective notebooks are Dim_Reduction_and_UMAP_Plotting and Random_BA_Picking.ipynb.

### Summarized Data

The ready-to-use .csv files are stored in this folder.

## Usage

For instructions on how you run the individual steps of this workflow refer to the README.md files in the individual folders.
