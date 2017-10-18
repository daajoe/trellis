# trellis
TREewidth LocaL Improvement Solver

is a decomposer that allows to compute [tree decompositions](https://en.wikipedia.org/wiki/Tree_decomposition)[1] of graphs given in the [PACE format]().

# Installation
See [INSTALL.md](INSTALL.md)

#License
- GPL3+
- subsolvers consult the repositories (see list below)


# How to run trellis?
- Output an upper bound on the treewidth of graph "graph.gr":
```bash
bin/trellis -f trellis/test/graphs/3x3-grid.edge
```

Trellis will output the statistics in [json format](https://en.wikipedia.org/wiki/JSON) into stdout.

- Output the decomposition into file with name "filename.td". 
```bash
bin/trellis -f trellis/test/graphs/3x3-grid.edge -o filename.td
```

- Use trellis as interface to a PACE solver.
```bash
bin/trellis -f graph.gr -o filename.td -gs HTD2017 -ni 0
```

- Output details on the parameters.
```bash
bin/trellis --help
```

- Output pcs file for [SMAC(Sequential Model-based Algorithm Configurattion)](https://automl.github.io/SMAC3/stable/manual.html) [2]
```bash
bin/trellis --pcs
```

# Make trellis less verbose
Edit file *bin/logging.conf* in the usual way.
Change ``level=INFO`` to ``level=ERROR`` results in error outputs only and the json statistics into stdout.


## Parameter description
### Main Parameters
| Parameter | Meaning|
|--- | --- |
| -ls NAME | Local solver|
| -gs NAME | Global solver |
| -ni INT | Number of no-improvement rounds|
| -gw INT | Global wall clock limit in seconds | 
| -la opt1| Options for the local solver {avaliable options are given in opt1/opt2/...}|
| -la opt1 | Options for the global solver {avaliable options are given in opt1/opt2/...}|
| -lb INT | Local budget (for the number of vertices we want to pick)
| -lw INT | Local wall clock limit in seconds|
| -lx INT | Local wall clock limit in seconds for a single sat call (only for jdrasil)| 


### Technical Parameters

| Parameter | Meaning|
|--- | ---|
| -t PATH | temporary folder|
| --pcs| Output pcs file for [SMAC(Sequential Model-based Algorithm Configurattion)](https://automl.github.io/SMAC3/stable/manual.html) |
| -f INSTANCE | Instance name| 

### Advanced Parameters for Algorithm Configuration
See bin/trellis --help


# How to reference?
When using trellis in academic papers please reference as:

#### Trellis
```bibtex
@inproceedings{FichteLodhaSzeider17a,
	Abstract = {Many hard problems can be solved efficiently for problem instances that can be decomposed by tree decompositions of small width. In particular for problems beyond NP, such as {\#}P-complete counting problems, tree decomposition-based methods are particularly attractive. However, finding an optimal tree decomposition is itself an NP-hard problem. Existing methods for finding tree decompositions of small width either (a) yield optimal tree decompositions but are applicable only to small instances or (b) are based on greedy heuristics which often yield tree decompositions that are far from optimal. In this paper, we propose a new method that combines (a) and (b), where a heuristically obtained tree decomposition is improved locally by means of a SAT encoding. We provide an experimental evaluation of our new method.},
	Address = {Melbourne, VIC, Australia},
	Author = {Fichte, Johannes K. and Lodha, Neha and Szeider, Stefan},
	Booktitle = {Proceedings on the 20th International Conference on Theory and Applications of Satisfiability Testing (SAT'17)},
	Date-Added = {2017-09-22 18:23:23 +0000},
	Date-Modified = {2017-09-22 18:24:19 +0000},
	Doi = {10.1007/978-3-319-66263-3_25},
	Editor = {Gaspers, Serge and Walsh, Toby},
	Isbn = {978-3-319-66263-3},
	Month = aug,
	Pages = {401--411},
	Publisher = {Springer Verlag},
	Title = {SAT-Based Local Improvement for Finding Tree Decompositions of Small Width},
	Year = {2017}
}
```

#### PACE2017
```bibtex
% The official bibliographic information is not available yet,
% but it should be close to the following:
@InProceedings{dell_et_al:LIPIcs:2018:PACEbestguess,
  author =	{Holger Dell and Christian Komusiewicz and Nimrod Talmon and Mathias Weller},
  title =	{{The PACE 2017 Parameterized Algorithms and Computational Experiments Challenge: The Second Iteration}},
  booktitle =	{12th International Symposium on Parameterized and Exact Computation (IPEC 2017)},
  pages =	{30:1--30:12},
  series =	{Leibniz International Proceedings in Informatics (LIPIcs)},
  year =	{2018},
  editor =	{Daniel Lokshtanov and Naomi Nishimura},
  publisher =	{Schloss Dagstuhl--Leibniz-Zentrum fuer Informatik},
  address =	{Dagstuhl, Germany},
  doi =		{10.4230/LIPIcs.IPEC.2017.30},
  annote =	{Keywords: treewidth, minimum fill-in, chordal completion, contest, implementation challenge, FPT}
}
```

#### PACE2016
```bibtex
@InProceedings{dell_et_al:LIPIcs:2017:6931,
  author =	{Holger Dell and Thore Husfeldt and Bart M. P. Jansen and Petteri Kaski and Christian Komusiewicz and Frances A. Rosamond},
  title =	{{The First Parameterized Algorithms and Computational Experiments Challenge}},
  booktitle =	{11th International Symposium on Parameterized and Exact Computation (IPEC 2016)},
  pages =	{30:1--30:9},
  series =	{Leibniz International Proceedings in Informatics (LIPIcs)},
  ISBN =	{978-3-95977-023-1},
  ISSN =	{1868-8969},
  year =	{2017},
  volume =	{63},
  editor =	{Jiong Guo and Danny Hermelin},
  publisher =	{Schloss Dagstuhl--Leibniz-Zentrum fuer Informatik},
  address =	{Dagstuhl, Germany},
  URL =		{http://drops.dagstuhl.de/opus/volltexte/2017/6931},
  URN =		{urn:nbn:de:0030-drops-69310},
  doi =		{10.4230/LIPIcs.IPEC.2016.30},
  annote =	{Keywords: treewidth, feedback vertex set, contest, implementation challenge, FPT}
}
```

# Subsolvers
Trellis suports the following solvers.

| Decomposer | Parameters (Names) | Exact |  Heuristic | Link (github) 
| --- | --- | --- | --- | ---
| *bztreewidth* | `BzTreewidth2016` |  | x | [TomvdZanden/BZTreewidth.git](https://github.com/TomvdZanden/BZTreewidth.git)
| *flowcutter* | `FlowCutter2016`| | x| [ben-strasser/flow-cutter-pace16.git](https://github.com/ben-strasser/flow-cutter-pace16.git) 
|  | ``FlowCutter2017``| | x| [kit-algo/flow-cutter-pace17.git](https://github.com/kit-algo/flow-cutter-pace17.git)  
| *jdrasil* |`Jdrasil2016`  | x| | [daajoe/Jdrasil.git (2016)](https://github.com/daajoe/Jdrasil/tree/sat_runtmlm)| |
| |`Jdrasil2017`  | x| x | [daajoe/Jdrasil.git (2017)](https://github.com/daajoe/Jdrasil/)| |
| |`JdrasilHeuristic2017`  | x| x | [daajoe/Jdrasil.git (2017)](https://github.com/daajoe/Jdrasil/)| |
| *htd* | `HTD2016`| | x| [mabseher/htd.git (2016)](https://github.com/mabseher/htd/releases/tag/v0.9.5-beta)  | decomposer/pace2016/htd
| | `HTD2017`| | x| [mabseher/htd.git (2017)](https://github.com/mabseher/htd/releases/tag/1.2)
| *tamaki* |`Tamaki2016`| x| | [TCS-Meiji/treewidth-exact.git](https://github.com/TCS-Meiji/treewidth-exact.git)
| | `Tamaki2017`| x| | [daajoe/PACE2017-TrackA.git](https://github.com/daajoe/PACE2017-TrackA.git)
| | ``TamakiHeuristic2017`` | | x| [daajoe/PACE2017-TrackA.git](https://github.com/daajoe/PACE2017-TrackA.git) 
| *tdLib* | `TdLib2017`| x| | [freetdi/p17.git](https://github.com/freetdi/p17.git)
| | `TdLibHeuristic2017`| | x| [freetdi/p17.git](https://github.com/freetdi/p17.git)
| *elithelli* | `Elithelli2016`| | x| [elitheeli/2016-pace-challenge.git](https://github.com/elitheeli/2016-pace-challenge.git) 
| *minfillbgmrs* | `Minfillbgmrs2017`| | x | [td-mrs/minfill_mrs.git](https://github.com/td-mrs/minfill_mrs.git)
| *minfillmrs*  | `Minfillmrs2017`| | x | [td-mrs/minfillbg_mrs.git](https://github.com/td-mrs/minfillbg_mrs.git)
| *mfjones* | `Mfjones2016`| | x| [mfjones/pace2016.git](https://github.com/mfjones/pace2016.git)
| *mrprajesh* | `Mrprajesh2016`| | x| [mrprajesh/pacechallenge.git](https://github.com/mrprajesh/pacechallenge.git)

Sub-solver sources will be fetched into the folder: *decomposer/year/solvername*

Sub-solvers will be installed after compiling into the folder: *lib/year/solvername* 



# FAQs
## My cmake is too old. How to upgrade?
On old Linux distributions you might need to upgrade your cmake >3.5
### Ubuntu
sudo apt-get install software-properties-common python-software-properties
sudo add-apt-repository ppa:george-edison55/cmake-3.x
sudo apt-get update
or
sudo apt-get upgrade

### Build from source
See for example 
- https://askubuntu.com/questions/355565/how-to-install-latest-cmake-version-in-linux-ubuntu-from-command-line
- https://askubuntu.com/questions/610291/how-to-install-cmake-3-2-on-ubuntu-14-04

curl https://cmake.org/files/v3.9/cmake-3.9.4.tar.gz -o cmake-3.9.4.tar.gz
tar xf cmake-3.9.4.tar.gz
cd cmake-3.9.4
./configure
make install


#Todos / Known bugs
## Bugfix
- make clean
- minimal version (without solvers that require gradle/jdk/mono)


# References
[1]: Bodlaender and Koster: Treewidth computations I. Upper bounds.  Journal Information and Computation (208/3). p. 259--275. 2010. [doi:10.1016/j.ic.2009.03.008](https://doi.org/10.1016/j.ic.2009.03.008)

[2]: Frank and Ramage: Manual for SMAC (Sequential Model-based Algorithm Configuration). Version v2.10.03-master. UBC. 2015.
 
[3]: Fichte, Lodha, Szeider:  SAT-Based Local Improvement for Finding Tree Decompositions of Small Width. SAT 2017. [doi:missing](https://doi.org/missing)