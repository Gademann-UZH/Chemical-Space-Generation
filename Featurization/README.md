# How to use Featurize.py

## What does it do?

Featurize.py reads in molecular structures in SMILES format from a dataset.txt file, converts them to .xyz files using [OpenBabel](http://openbabel.org/wiki/Main_Page), and performs a conformational search for the lowest energy using [XTB](https://xtb-docs.readthedocs.io/en/latest/setup.html), and [CREST](https://xtb-docs.readthedocs.io/en/latest/crest.html). With the lowest energy conformer .xyz file and the geometry optimization (_geo_opt) header and footer a ORCA input file is generated and a geometry optimization is performed. With this geometry a next ORCA input file is generated for the first part of the featurization. The features to be calculated are defined in the header and footer. The results of this first featurization are saved in a folder structure and is used by the second part. The second part uses also the [Multiwfn](http://sobereva.com/multiwfn/) program.

## Step-by-step

### 1) Install OpenBabel, ORCA, XTB, CREST, and Multiwfn

For the installation of these programs there are various options and possibilities, which all depend on the OS you use and personal preferences. In our case, the featurization was performed on the UZH science cloud and hence installed from pre-compiled binaries on Linux. Additionally, the installation can be performed with Conda.

### 2) Adjust the header & footer files

Before you start, update the header and footer files and adjust them to your preferences.

These files are used for the ORCA input file generation and hence control which functionals and basis sets are used. By default, the geometry optimization uses the B97-3c density functional method and the featurization the ωB97X-D3 functional with the def2-tzvp basis set.

Some of the properties which are calculated during featurization have to be explicitly defined in the header (i.e. Hirshfeld charges) and footer (i.e. chemical shielding). You can additionally add properties you want calculated. HOWEVER!, be aware that if you do you will need to update the Featurize.py code to tell the parser to look for your data. Otherwise it will be calculated but ignored afterwards (**see section XY**). 

Make sure to update the "Nprocs" value in the header files. This value defines how many cores are available to the various programs we run and will cause problems if set too high and long calculation times if set too low.

### 3) Folder preparation

Place the Featurization folder in your preferred directory and rename it to a meaningfull name.

### 4) Adjust the Featurize.py script

Similar to the header and footer files, the script itself has to be tweaked depending on your dataset etc. At the very top in the "CONSTANTS" section define the path pointing to where ORCA is installed on your machine. Again specify the number of cores available on your machine. This has to be defined here as well, since XTB and CREST do not read this value from the header files.

### (Optional) Update the parser in the Featurize.py script

Sample text