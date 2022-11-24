# How to use random substrate picking?

## What does it do:
The **Random_BA_Picking.ipynb** notebook reads in data from a summarized .csv file, generates a chemical space, and picks one random substrate from every cluster. Hence, the initial portion of code is quite similar to the **Dim_Reduction_and_UMAP_Plotting.ipynb:** script. Since additional information is given there please refer to the corresponding README file if needed.

## Step-by-step

### 1) Setup

The use of the **Random_BA_Picking.ipynb** Jupyter Notbook requires the installation of various python packages, for processing data as well as for depicting the outcomes. Hence, make sure to install [pandas](https://anaconda.org/anaconda/pandas), [numpy](https://anaconda.org/anaconda/numpy), [umap](https://anaconda.org/conda-forge/umap-learn), [sklearn](https://anaconda.org/anaconda/scikit-learn), [scipy](https://anaconda.org/anaconda/scipy), [rdkit](https://anaconda.org/conda-forge/rdkit), [ipython](https://anaconda.org/anaconda/ipython), [seaborn](https://anaconda.org/anaconda/seaborn), and [matplotlib](https://anaconda.org/conda-forge/matplotlib). While it is up to you how to install these, conda makes it very easy. The conda installation commands are linked.

For the **Dim_Reduction_and_UMAP_Plotting:** notebook to work without changing code, make sure that the summarized_data.csv is present in the same folder.

### 2) Step-by-step

1) Run block one to import all necessary modules.

2) Run block two to read in all data from the desiganted .csv file. By changing the file name in the "with open" line at the top of the block you can specify which .csv file to use.

3) The third block generates the embeddings, evaluates them, and finally picks the "best" one. At the top of this block are a few parameters we can adjust. The parameters "dims", "ns", and "seeds" MUST be all arrays. If you know from which embedding you want to pick random substrates you can exactly specify the values to save time. In case you first need to find a suitable embedding, below is an explanation fo what to do.

- dims: holds all target dimensionalities for which an embedding should be generated. Its values must be at least 2 and at most equal to the initial dimensionality of the dataset (i.e. the number of substrate parameters used for UMAP).
- ns: are the nearest_neighbor values to be tested. The values must be >1 and should not be too large. By default, the value is calculated as the square root of the initial dataset dimensionality, which was suggested by [Doyle and co-workers](https://doi.org/10.1021/jacs.1c12203) and also worked fine in our case.
- seeds: These values describe the initial seed value which is used for rng and can be any number. Changes in this value should not impact the overall appearance of the chemical space too drastically and are more a tool for fine tuning.

Next, we have to tell UMAP which featurized parameters should be considered. To do so, simply comment or uncomment entries in the "umap_data" structure. In case you chose to calculate additional parameters during featurization, you can simply add a new entry to "umap_data" which specifies the abbreviation chosen for this parameter. 

Why you should not use all parameters: Using or not using certain parameters can heavily influence the outcome of the UMAP. As such testing different combinations of parameters is important. Also this will yield information of which parameters have a significant impact and are crucial for achieving good clustering and which do not.

Now that everything is set up, run the fourth block. Depending on the number of embeddings it needs to generate and evaluate this might take a few minutes. After all embeddings are generated, they will be evaluated by Silhouette scores. To do so, the algorithm tries to group datapoints in each embedding into x clusters, where x starts at 10 and iteratively increases up to 30. This range is defined in the "N_CLS_list" variable. While the top and bottom value can be changed, this range worked well in our case.

During this rating process, it keeps track of all scores and the respective values for dimensionality, number of nearest_neighbors, seed, and number of clusters. Finally, this is used to find the highest scoring combination.

Then, it will take the embedding with the highest score and generate a dendrogram for it with the "optimal" number of clusters. The dendrogram already shows how many members each cluster has and if they are rather evenly distributed or clumped in a few clusters.

Finally, the clustered chemical space based on the highest scoring embedding is plotted. By default, each cluster is shown in a different color (palette = "rainbow"). However, the color scheme can be eaasily adjusted by changing the "palette" argument value in the sns.scatterplot() function. Here is an extensive overview of available [seaborn colorschemes](https://medium.com/@morganjonesartist/color-guide-to-seaborn-palettes-da849406d44f).

**IMPORTANT TO NOTE**: The code keeping track of the "best" Silhouette score is extremely simple and only checks for which combination of arguments the highest value is achieved. It has no idea of trends or outliers, which may cause a bad embedding to be picked for plotting. Hence, iterating over steps 3) to 5) is advised.

4) If you are happy with the chemical space, you can run the last block of code. It will group the dataset according to the clustering and pick one example from each cluster. Itb will also retrieve their coordinates within the chemical space and then output the structures of all picked substrates and a chemical space map which shows the picked substrates as stars.
