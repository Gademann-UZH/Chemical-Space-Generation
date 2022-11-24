# How to generate a chemical space

## What does it do?

The **Dim_Reduction_and_UMAP_Plotting:** notbook, reads in pre-compiled featurization data in .csv format (see the **Summarized_Data** folder) and generates a chemical space using the [Uniform Manifold Approximation and Projection (UMAP)](https://github.com/lmcinnes/umap). Furthermore, it can be used to plot the resulting clusters in various ways. After reading in the summarized data it is passed to the UMAP algorithm, which reduces the initial dimensionality of the dataset to a target dimensionality. This is referred to as dimensionality reduction, since the target dimensionality is always lower than the inital one. The output of this process is called an embedding. In this case, multiple embeddings are generated, varying input arguments which will be discussed in more detail below. These embeddings are then evaluated by means of Silhouette scores, and clustered. The result can be plotted and is then referred to as a n dimensional chemical space. Finally, the script contains a few options on how to plot the generated chemical space. This options are fairly specific to [this project](https://doi.org/10.1021/acscatal.2c01813), however, they can be easily adapted and expanded.

This script is based on resources for which a detailed explanation is beyond the scope of this how-to. However, here you find additional information about:

UMAP: [documentation](https://umap-learn.readthedocs.io/en/latest/), [interactive "simple" explanation](https://pair-code.github.io/understanding-umap/)        
Silhouette scores: [publication](https://doi.org/10.1016/0377-0427(87)90125-7), [implementation in python](https://towardsdatascience.com/silhouette-coefficient-validating-clustering-techniques-e976bb81d10c)

## Step-by-step

### 1) Setup

The use of the **Dim_Reduction_and_UMAP_Plotting:** Jupyter Notbook requires the installation of various python packages, for processing data as well as for depicting the outcomes. Hence, make sure to install [OpenBabel](https://anaconda.org/conda-forge/openbabel), [pandas](https://anaconda.org/anaconda/pandas), [numpy](https://anaconda.org/anaconda/numpy), [umap](https://anaconda.org/conda-forge/umap-learn), [sklearn](https://anaconda.org/anaconda/scikit-learn), [scipy](https://anaconda.org/anaconda/scipy), [rdkit](https://anaconda.org/conda-forge/rdkit), [ipython](https://anaconda.org/anaconda/ipython), [seaborn](https://anaconda.org/anaconda/seaborn), and [matplotlib](https://anaconda.org/conda-forge/matplotlib). While it is up to you how to install these, conda makes it very easy. The conda installation commands are linked.

For the **Dim_Reduction_and_UMAP_Plotting:** notebook to work without changin code, make sure that the summarized_data.csv is present in the same folder. If you plan on plotting substrates on top of the chemical space the respective compound lists have to be added to the same folder as well. This lists are .txt holding the compound structures in inchi format. 

### 2) Run the script

1) Run the first block to import all necesary modules

2) Run the second block to read in the data from a .csv file and populate the "plot_data" dictionary At the same time this will generate the array "inchis" populate it. Since this is done via OpenBabel and the command line its a bit slower. The array will be used later to depict compound structures.

3) The third block generates the embeddings, evaluates them, and finally picks the "best" one. At the top of this block are a few parameters we can adjust. The parameters "dims", "ns", and "seeds" MUST be all arrays. 

- dims: holds all target dimensionalities for which an embedding should be generated. Its values must be at least 2 and at most equal to the initial dimensionality of the dataset (i.e. the number of substrate parameters used for UMAP).
- ns: are the nearest_neighbor values to be tested. The values must be >1 and should not be too large. By default, the value is calculated as the square root of the initial dataset dimensionality, which was suggested by [Doyle and co-workers](https://doi.org/10.1021/jacs.1c12203) and also worked fine in our case.
- seeds: These values describe the initial seed value which is used for rng and can be any number. Changes in this value should not impact the overall appearance of the chemical space too drastically and are more a tool for fine tuning.

Next, we have to tell UMAP which featurized parameters should be considered. To do so, simply comment or uncomment entries in the "umap_data" structure. In case you chose to calculate additional parameters during featurization, you can simply add a new entry to "umap_data" which specifies the abbreviation chosen for this parameter. 

Why you should not use all parameters: Using or not using certain parameters can heavily influence the outcome of the UMAP. As such testing different combinations of parameters is important. Also this will yield information of which parameters have a significant impact and are crucial for achieving good clustering and which do not.

Now that everything is set up, run the fourth block. Depending on the number of embeddings it needs to generate and evaluate this might take a few minutes. After all embeddings are generated, they will be evaluated by Silhouette scores. To do so, the algorithm tries to group datapoints in each embedding into x clusters, where x starts at 10 and iteratively increases up to 30. This range is defined in the "N_CLS_list" variable. While the top and bottom value can be changed, this range worked well in our case.

During this rating process, it keeps track of all scores and the respective values for dimensionality, number of nearest_neighbors, seed, and number of clusters. Finally, this is used to find the highest scoring combination.

4) Running the next block of code will take the embedding with the highest score and generate a dendrogram for it with the "optimal" number of clusters. The dendrogram already shows how many members each cluster has and if they are rather evenly distributed or clumped in a few clusters.

5) The few lines of code in the next block plot the clustered chemical space based on the highest scoring embedding. By default, each cluster is shown in a different color (palette = "rainbow"). However, the color scheme can be eaasily adjusted by changing the "palette" argument value in the sns.scatterplot() function. Here is an extensive overview of available [seaborn colorschemes](https://medium.com/@morganjonesartist/color-guide-to-seaborn-palettes-da849406d44f).

5.5) **IMPORTANT TO NOTE**: The code keeping track of the "best" Silhouette score is extremely simple and only checks for which combination of arguments the highest value is achieved. It has no idea of trends or outliers, which may cause a bad embedding to be picked for plotting. Hence, iterating over steps 3) to 5) is advised. 

**OPTIONAL**

6) The next block of code can be used to read in multiple sets of substrates to then plot them on top of the chemical space. The lists provided for this should be in .txt format and contain all substrates as inchis. In code, adjust the name of the files you want to read in and comment out or remove the segments of "with open" commands you do not need. Then run the block of code. It will check whether the provided inchis are present within the chemical space dataset and will let you know how many and which were found by means of their index in the dataset.txt file. The found compound indeces are stored in the "index_groups" dictionary and are used to identify substrates within the "plot_data" dictionary.

7) Run the next block to retrieve the partial data from the optimal embedding. The default setup will generate groupings of the clusters specific to this project. Feel free to modify this as you need.

8) Now that we have the coordinates of the substrates we want to plot on the chemical space, we can do so. As mentioned in 7) the visuals of this will greatly depend on the grouping, which can be modified as needed. The same is true for the markers (stars) and the color scheme. For more information on modifying the color scheme refer to 5).

9) The next block shows how plotting with a different grouping might look like. In this case, clusters are grouped depending on reactivity and markers (stars) are colored according to the substrate set we read-in in 6). Additionally, each marker is labeled with the index of the substrate within the dataset.txt file, ich_list.txt file, or assigned_list.txt file obtained from the featurization. 

10) The last cluster can be used to display n members of each cluster (or the whole cluster if n is larger than the cluster size). To do so we define the "n_per_cluster" variable to say how many examples per cluster should be displayed and run the block of code. If the specified line is uncommended all images generated this way will be saved:

- pic.save(f"Cluster_{group}.png")





