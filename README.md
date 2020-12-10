# Featurizer

This repository contains the code used in

Mayer, C. and Daland, R. (2020). A method for projecting features from observed sets of phonological classes. *Linguistic Inquiry, 51*(4). 

You can find a pre-print of the paper [here](https://linguistics.ucla.edu/people/grads/connormayer/papers/cmayer_rdaland_projecting_features_revised.pdf) and the final version [here](https://www.mitpressjournals.org/doi/abs/10.1162/ling_a_00359).

This code is made publicly available for use and extension in future research. I'm happy to help with troubleshooting any issues you might encounter.

The basic functionality of this code is to take a set of input phonological classes and produce a feature system for that set. See the paper for a full description.

This program can be run with either a graphical user interface (GUI; implemented by [Isaac Lee](https://github.com/eyezhick)) or a command line interface. Instructions for each can be found below.

---

## Requirements

Python requirements (other versions will probably work, but have not been tested):

* Python 3 (3.8.2)
* `numpy` package (1.17.4) (optional, but much more efficient)
* `tkinter` package (8.6) (optional, but required to use GUI)
* `graphviz` package (0.8.4) (optional, but required to generate `.png` outputs)

Other requirements

* Graphviz (2.4.11) (optional, but required to generate `.png` outputs): In order to generate `.png` images, you will also need to have Graphviz installed on your system. This is in addition to the `graphviz` Python library mentioned above, which just provides an interface between Python and Graphviz. You can download Graphviz [here](https://graphviz.org/download/).

## Input and output formats

* Input: A file which contains a set of phonological classes. Classes should be separated by a new line, and each member of the class must be separated by a space. The first line in the file must be the full alphabet. See the files in `sample_inputs` for examples.
* Ouput: In addition to printing output to the command line or text window, this program produces five types of output files:
    * A `.csv` file containing the segments and their generated features. This is stored by default in `csv_output`.
    * A `.gv` file containing a graph of the final intersectional closure of the input class system once the featurization has been done. By default this is stored in `poset_output`. See below for how to convert these to image files.
    * A `.gv` file containing a feature graph of the final intersectional closure of the input class system after featurization. This is similar to the class diagram above, but also includes the feature/value pairs associated with each class. See below for how to convert these to image files.
    * A `.png` rendering of the poset graph.
    * A `.png` rendering of the feature graph.
    
## Running the graphical user interface

You can run the program using a graphical user interface (GUI) by running `main.py` in the `code` directory. You can do so either via the command line by typing `python3 main.py` or by opening the script using Python. On Windows, for example, you can right click on `main.py`, choose `Open with` and then choose `Python` or `Python 3.X`. 

You must choose an input class file by clicking `Browse` under the `Select a file` section.

The `Featurization type` and `Options` section allow you to specify aspects of how the featurization of the input classes is carried out.

* `Featurization type`: Determines the process by which the features are calculated. See the paper for details about each method.
* `Options`:
   ** `numpy`: If this box is checked, the `numpy` package will be used for matrix operations. This requires `numpy` to be installed. Otherwise, a bespoke, less efficient matrix implementation will be used. Note that the bespoke implementation is *significantly* slower, and may take quite a while for large inputs.
   ** `verbose`: If this box is checked, additional intermediate information will be printed as the algorithm is run. This only affects the output of the `print` button.
   
The `Save a file` section allows you to save or print the output of the algorithm in various formats:

* `Featurization graph as PNG/GV` allow you to save a `.png`/`.gv` version of the featurization graph, respectively.
* `Poset graph as PNG/GV` allow you to save a `.png`/`.gv` version of the poset graph, respectively.
* `CSV` allows you to save a CSV representation of the derived feature system.
* `print` prints the output of the algorithm to a text window. This doesn't actually save anything.

## Running from the command line

The program can be run from the command line by running the `Featurizer.py` script. 

Command line arguments:

* Required positional argument: The path to the input class file.
* `--output_file`: The path where the output `.csv` file will be saved. Optional, default `../csv_output/features.csv`.
* `--featurization`: The type of featurization to use. Must be one of `privative`, `complementary`, `inferential_complementary`, or `full`. Optional, default `complementary`.
* `--use_numpy`: If this flag is provided, the `numpy` package will be used for matrix operations. This requires `numpy` to be installed. Otherwise, a bespoke, less efficient matrix implementation will be used. Note that the bespoke implementation is *significantly* slower, and may take quite a while for large inputs.
* `--poset_file`: The path where the output class system graph will be saved. Optional, default `../poset_output/poset_graph.gv`.
* `--feats_file`: The path where the output feature graph will be saved. Optional, default `../feats_output/feats_graph.gv`.
* `--verbose`: If this flag is provided, additional intermediate information will be printed to the console as the algorithm is run.

Currently running from the command line will only output `.gv` versions of the poset and feature graphs. These must be manually converted to `.png` files using the steps described below, or by using the GUI interface

## code

This folder contains the code used in the paper.

**main.py**: Contains the code for the graphical user interface.

**Featurizer.py**: Takes a file containing a set of phonological classes as input, and produces a featurization of that set. Can be called from the command line, or imported and used in a Python script.

**Poset.py**: Implements a partially ordered set. Maintains the basic partial ordering of the class system (parent/child), and calculates the intersectional closure, among other things. No command line interface.

**Array.py**: A bespoke implementation that duplicates the subset of the functionality of `numpy` arrays that is necessary for this program. Included to improve code portability, but things will run *much* faster if you install `numpy` and use the `--use_numpy` flag described above.

## sample_inputs

A folder containing some example class input files, including all examples discussed in the paper.

## csv_output

A folder for saving output `.csv`s containing segment feature mappings.

## poset_output

A folder for saving output poset graphs.

## feats_output 

A folder for saving feature output graphs.

---

## Generating images from Graphviz (`.gv`) files

The class structure and feature diagrams can be saved as Graphviz `.gv` files. These files are useful because they can be easily modified to customize the graphs (all diagrams in the paper were made by this process). To convert the files to an image format like a `.png`, you can use the `dot` program, which you may have to install. See the [dot manual](https://www.graphviz.org/doc/info/command.html) for details.

For example, you can convert a `.gv` file to a `.png` by running:

```dot -Tpng -O my_graphviz_file.gv```

---


